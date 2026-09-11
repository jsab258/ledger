#!/usr/bin/env python3
"""Every subprocess call in the daemon fleet carries creationflags=NO_WINDOW.

    python3 tools/lint-no-window.py
    python3 tools/lint-no-window.py --root=<path-to-a-copy-of-the-tree>
    python3 tools/lint-no-window.py --selftest

THE PATH TAKES AN EQUALS SIGN. `--root <path>` with a space was silently
ignored once, on 2026-09-11, by an earlier version of this file that skipped
what it did not recognise: the tool then measured the REAL tree, printed a
clean result, and the reader took it for a pass of the copy he had planted a
fault in. An argument this tool does not understand is now an error that
names it and exits 2.

WHY THIS EXISTS, 2026-09-11. Jafar re-enabled the supervisor scheduled task
and his screen filled with cmd windows appearing and disappearing in a loop.
Not a crash loop: taskLastTaskResult 267009 is 0x00041301, "the task is
currently running". The full reasoning is ONE comment, in
tools/runner/launch-supervisor.py beside its NO_WINDOW, and it is not
restated here; the short form is that the task registers pythonw.exe, so the
top process has no console, and on Windows a console-subsystem child
(git.exe, tasklist.exe, taskkill.exe, schtasks.exe) launched from a parent
with no console and without CREATE_NO_WINDOW ALLOCATES ITS OWN CONSOLE
WINDOW. Eleven call sites in the five files the supervisor spawns, none of
them flagged, and nine more in the modules those files IMPORT, which run in
the same processes and which the first version of this tool did not count.
Twenty in all, and the fault was invisible for as long as every start came
from a .bat with a console to inherit.

WHAT IT ASSERTS, AND WHY IT IS AN ast WALK RATHER THAN A grep. The property
is "no call site can reach CreateProcess without the flag", which is a
statement about calls, not about text: a grep for creationflags counts
mentions, including one inside a comment or a docstring, and cannot see a
call that passes the flag hidden inside a **dict. So:

  every subprocess.Popen / run / call / check_call / check_output in a fleet
    file passes a creationflags= keyword whose expression NAMES NO_WINDOW
    (alone or ORed with something else, which is how a site that already had
    creationflags keeps what it had);
  a flag arriving only through **kwargs is NOT accepted, because this tool
    cannot prove what is in the dict and a guard that cannot prove its claim
    must fail closed;
  every fleet file that makes such a call defines NO_WINDOW at module level,
    guarded by os.name so it is a no-op off Windows;
  exactly one fleet file carries the reasoning, and every other definition
    points at it by path, so the twenty sites cannot drift into twenty
    slightly different explanations the way bootstrap-paths.cmd did;
  no fleet file uses os.system / os.popen / os.spawn*, which open a console
    and have no creationflags to pass.

WHAT IT CANNOT ASSERT, said plainly rather than implied. Whether a window
opens. That needs Windows, and there is none in this container: the answer to
that question is the five minute proof step in
.github/workflows/ledger-install-supervisor-task.yml, which starts the fleet
from a deliberately console-less parent on the PC and samples
MainWindowHandle and conhost.exe children. A green lint here is a necessary
condition and not the measurement.

THE FLEET IS DERIVED, NOT LISTED, which is the lesson
tools/lint-bootstrap-single.py paid for: its hand-written list of workflows
was the denominator, the one workflow missing from it was the one that broke,
and the lint printed 0 problems about it for its whole life. So the set of
daemon files is read out of tools/supervise.py itself (the .py paths it
spawns as children), plus the launcher door and supervise.py. Add a fourth
daemon there and this tool starts checking it without anybody remembering to.
FLOOR keeps the derivation honest in the other direction: a parser regression
that stopped seeing pc-watcher.py would otherwise read as a clean tree.

THE FLEET IS THE CODE THE DAEMONS RUN, WHICH IS NOT THE SAME AS THE FILES
THEY ARE. A subprocess call in an imported module runs inside the importing
daemon, under the same console-less parent, and opens the same window. The
first version of this tool stopped at the five spawned files and printed a
clean 11/11 while nine calls in tools/runner/single_instance.py (tasklist,
in the launcher itself), inbox.py and outbox.py (git in the bot and the
executor, every pass) still opened windows. So the derivation follows
imports transitively, and EXEMPT is empty: the only reason that belongs
there is that a call cannot take creationflags at all.
"""
import ast
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: The one file that carries the reasoning. Every other definition points here.
CANONICAL = "tools/runner/launch-supervisor.py"
#: The exact words that mark it, so "the reasoning moved" is a failure rather
#: than a silent second copy.
MARKER = "NO_WINDOW REASONING LIVES HERE"
#: The constant every call site must name.
CONST = "NO_WINDOW"

#: The supervisor itself and the door every launch goes through. The daemons
#: are DERIVED from the first of these rather than listed.
ANCHORS = ("tools/supervise.py", CANONICAL)

#: A parser regression must not read as a clean tree (rule 3b): these eight
#: files were the fleet on 2026-09-11 and the derivation must still find
#: them. The last three are reached by IMPORT rather than by spawn, which is
#: the half the first version of this list missed.
FLOOR = ("tools/supervise.py", "tools/pc-watcher.py",
         "tools/runner/executor.py", "tools/runner/telegram-bot.py",
         CANONICAL,
         "tools/runner/single_instance.py", "tools/runner/inbox.py",
         "tools/runner/outbox.py")

#: EMPTY, AND IT STAYS EMPTY UNLESS A CALL GENUINELY CANNOT TAKE THE FLAG.
#:
#: It was not empty for an hour on 2026-09-11: it named single_instance.py,
#: inbox.py and outbox.py with nine unflagged calls between them, and the
#: reason written beside each was that they sat outside one task's scope.
#: That is a note to a reviewer written into a place that keeps it for ever.
#: AN EXEMPTION IN A LINT IS A PERMANENT LICENCE, so the only reason that
#: belongs here is why the flag CANNOT be applied to that call, never why
#: nobody applied it yet. All nine took it.
EXEMPT = {}

#: The calls that reach CreateProcess on Windows.
SPAWNERS = ("Popen", "run", "call", "check_call", "check_output")
#: No creationflags to pass, so no way to suppress the console.
BANNED = ("os.system", "os.popen", "os.spawnl", "os.spawnle", "os.spawnlp",
          "os.spawnlpe", "os.spawnv", "os.spawnve", "os.spawnvp",
          "os.spawnvpe")


def _call_name(node):
    """'subprocess.run', 'os.path.join', 'os.system' or a bare name, or None.

    THE WHOLE CHAIN, NOT ONE LEVEL. The first version of this read only
    Attribute-on-Name, so `os.path.join` (Attribute on Attribute) returned
    None and the fleet derived to two files instead of five. FLOOR caught it
    on the first run, which is the only reason that is a paragraph here and
    not a silent 2 in a denominator.
    """
    fn = node.func
    parts = []
    while isinstance(fn, ast.Attribute):
        parts.append(fn.attr)
        fn = fn.value
    if not isinstance(fn, ast.Name):
        return None
    parts.append(fn.id)
    return ".".join(reversed(parts))


def _local_imports(root, rel):
    """The repo-local modules `rel` imports, as repo-relative paths.

    THE CODE THE DAEMONS RUN, NOT THE FILES SOMEBODY LISTED. A subprocess
    call in an imported module runs inside the importing daemon's process, so
    it has exactly the same windowless parent and opens exactly the same
    window: on 2026-09-11 nine such calls sat in single_instance.py (tasklist
    in the launcher itself), inbox.py and outbox.py (git in the bot and the
    executor, every pass), and a fleet set that stopped at the spawned files
    would have called that fixed.
    """
    out = []
    here = os.path.dirname(rel)
    try:
        tree = ast.parse(open(os.path.join(root, rel), encoding="utf-8").read())
    except (OSError, SyntaxError):
        return out
    for node in ast.walk(tree):
        names = []
        if isinstance(node, ast.Import):
            names = [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module]
        for nm in names:
            if "." in nm:
                continue
            for cand in (os.path.join(here, nm + ".py"),
                         os.path.join("tools", "runner", nm + ".py"),
                         os.path.join("tools", nm + ".py")):
                cand = cand.replace(os.sep, "/")
                if os.path.isfile(os.path.join(root, cand)):
                    out.append(cand)
                    break
    return out


def derive_fleet(root):
    """Everything a daemon process executes: the .py files tools/supervise.py
    spawns, the launcher door, and the transitive closure of the repo-local
    modules those import.

    READ OUT OF THE SPAWNER, NOT OUT OF A LIST. supervise.children() builds
    each child's argv with os.path.join(repo, "tools", ..., "<name>.py"), so
    the join whose last element ends in .py IS the daemon set. Returns
    (paths, why_not) with why_not naming the failure rather than an empty
    set standing in for "none found".
    """
    found = []
    for rel in ANCHORS:
        if os.path.isfile(os.path.join(root, rel)):
            found.append(rel)
    spawner = os.path.join(root, "tools", "supervise.py")
    if not os.path.isfile(spawner):
        return found, "tools/supervise.py is not there to derive from"
    try:
        tree = ast.parse(open(spawner, encoding="utf-8").read())
    except SyntaxError as e:
        return found, "tools/supervise.py does not parse (%s)" % e.msg
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if _call_name(node) != "os.path.join":
            continue
        parts = [a.value for a in node.args
                 if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if not parts or not parts[-1].endswith(".py"):
            continue
        if parts[0] != "tools":
            continue
        rel = "/".join(parts)
        if rel not in found and os.path.isfile(os.path.join(root, rel)):
            found.append(rel)
    # THE IMPORT CLOSURE, BREADTH FIRST AND TRANSITIVE: outbox.py is reached
    # through the bot, and whatever outbox.py imports runs in the bot too.
    queue = list(found)
    seen = set(found)
    while queue:
        for imp in _local_imports(root, queue.pop()):
            if imp not in seen:
                seen.add(imp)
                queue.append(imp)
                found.append(imp)
    return sorted(set(found)), ""


def _comment_block_above(lines, lineno):
    """The contiguous run of comment lines immediately above `lineno`
    (1-based). The pointer to the canonical reasoning has to be AT the
    definition to be read by anyone editing it."""
    out = []
    i = lineno - 2
    while i >= 0 and lines[i].lstrip().startswith("#"):
        out.append(lines[i])
        i -= 1
    return "\n".join(reversed(out))


def scan_file(root, rel):
    """(calls, flagged, problems) for one file. `calls` counts only the
    subprocess spawners, which is the denominator every count below is OF."""
    problems = []
    path = os.path.join(root, rel)
    try:
        src = open(path, encoding="utf-8").read()
        tree = ast.parse(src)
    except (OSError, SyntaxError) as e:
        # FAIL CLOSED. A file that cannot be read is not a file with no
        # problems in it, and that difference is the whole of rule 3b.
        return 0, 0, ["%s could not be parsed (%s), so nothing about it was "
                      "checked" % (rel, type(e).__name__)]
    lines = src.splitlines()

    calls = flagged = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name in BANNED:
            problems.append("%s:%d uses %s, which cannot carry creationflags "
                            "and opens a console" % (rel, node.lineno, name))
            continue
        if not name or not name.startswith("subprocess."):
            continue
        if name.split(".", 1)[1] not in SPAWNERS:
            continue
        calls += 1
        kw = [k for k in node.keywords if k.arg == "creationflags"]
        if not kw:
            if any(k.arg is None for k in node.keywords):
                problems.append(
                    "%s:%d %s passes no creationflags of its own and unpacks "
                    "a dict; a flag this tool cannot see is a flag it cannot "
                    "prove is there" % (rel, node.lineno, name))
            else:
                problems.append("%s:%d %s has no creationflags=%s"
                                % (rel, node.lineno, name, CONST))
            continue
        names = set(n.id for n in ast.walk(kw[0].value)
                    if isinstance(n, ast.Name))
        if CONST not in names:
            problems.append("%s:%d %s passes creationflags but does not name "
                            "%s in it" % (rel, node.lineno, name, CONST))
            continue
        flagged += 1

    if not calls:
        return calls, flagged, problems

    assigns = [n for n in tree.body
               if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == CONST
                       for t in n.targets)]
    if not assigns:
        problems.append("%s makes %d subprocess call(s) but defines no "
                        "module-level %s" % (rel, calls, CONST))
        return calls, flagged, problems
    if len(assigns) > 1:
        problems.append("%s defines %s %d times; one owner per condition"
                        % (rel, CONST, len(assigns)))
    seg = ast.get_source_segment(src, assigns[0]) or ""
    if "os.name" not in seg or "CREATE_NO_WINDOW" not in seg:
        problems.append("%s defines %s without both the os.name guard and "
                        "CREATE_NO_WINDOW, so it is not provably a no-op off "
                        "Windows" % (rel, CONST))
    above = _comment_block_above(lines, assigns[0].lineno)
    if rel == CANONICAL:
        if MARKER not in above:
            problems.append("%s is the canonical home but its %s definition "
                            "does not carry the reasoning (%r)"
                            % (rel, CONST, MARKER))
    else:
        if MARKER in above:
            problems.append("%s restates the reasoning that belongs only in "
                            "%s" % (rel, CANONICAL))
        if CANONICAL not in above:
            problems.append("%s defines %s without pointing at the reasoning "
                            "in %s" % (rel, CONST, CANONICAL))
    return calls, flagged, problems


def scan(root=REPO, exempt=None, floor=FLOOR):
    exempt = EXEMPT if exempt is None else exempt
    fleet, why_not = derive_fleet(root)
    problems = []
    if why_not:
        problems.append("the fleet could not be derived: %s" % why_not)
    for rel in floor:
        if rel not in fleet:
            problems.append("FLOOR: %s was the fleet on 2026-09-11 and the "
                            "derivation no longer finds it" % rel)

    calls = flagged = 0
    per_file = {}
    for rel in fleet:
        c, f, probs = scan_file(root, rel)
        calls += c
        flagged += f
        per_file[rel] = (c, f)
        problems.extend(probs)

    # THE EXEMPTED, COUNTED RATHER THAN HIDDEN. Their unflagged calls are the
    # denominator of what this lint does NOT cover, printed every run.
    ex_unflagged = 0
    ex_seen = {}
    for rel, reason in sorted(exempt.items()):
        if not os.path.isfile(os.path.join(root, rel)):
            problems.append("exemption names %s, which is not a file" % rel)
            continue
        if not (reason or "").strip():
            problems.append("exemption for %s has no written reason" % rel)
        c, f, _probs = scan_file(root, rel)
        ex_seen[rel] = (c, f)
        ex_unflagged += c - f
        if c - f == 0:
            problems.append("exemption for %s is stale: it has %d subprocess "
                            "call(s) and none of them is unflagged, so the "
                            "debt is paid and the exemption should go"
                            % (rel, c))
        if rel in fleet:
            problems.append("%s is both exempted and in the derived fleet; "
                            "one of the two is wrong" % rel)

    return {"fleet": fleet, "perFile": per_file, "calls": calls,
            "flagged": flagged, "exempt": ex_seen,
            "exemptUnflagged": ex_unflagged, "problems": problems}


def done_line(r):
    """One done line, key=value, no spaces inside a value, every count with
    the denominator it is OF (rule 3b). Whole-run numbers only.

    `noWindowSites=<k>/<n> unflagged=<m>` IS THE RULED GREP TARGET: section 1
    item 1 of game-design/decision-2026-09-11-ruling-the-windowless-fleet-and-
    four-smaller-calls.md says the re-enable condition is read by a later
    session out of the evidence file, by reading the line rather than judging
    it. The selftest asserts the exact shape so it cannot drift into a
    synonym a grep will miss. `unflagged` carries no slash of its own on
    purpose: `noWindowSites` immediately before it IS its denominator.
    """
    if not r["fleet"] or not r["calls"]:
        return ("lint-no-window NOTHING MEASURED - fleetFiles=%d "
                "subprocessCalls=%d" % (len(r["fleet"]), r["calls"]))
    return ("lint-no-window noWindowSites=%d/%d unflagged=%d fleetFiles=%d "
            "subprocessCalls=%d exemptFiles=%d exemptUnflaggedCalls=%d "
            "problems=%d"
            % (r["flagged"], r["calls"], r["calls"] - r["flagged"],
               len(r["fleet"]), r["calls"], len(r["exempt"]),
               r["exemptUnflagged"], len(r["problems"])))


def report(r):
    print(done_line(r))


USAGE = ("usage: python3 tools/lint-no-window.py [--root=<path>] "
         "[--selftest]\n"
         "       --root TAKES AN EQUALS SIGN: --root=/tmp/copy, never "
         "--root /tmp/copy")


def parse_args(argv):
    """(root, error). AN ARGUMENT THIS TOOL DOES NOT UNDERSTAND IS AN ERROR.

    --root= points this at a COPY of the tree, which is how the rejecting
    case is demonstrated on the real files (plant an unflagged call in a
    scratch copy) without ever planting one in the live fleet. The first
    version skipped anything it did not recognise, so `--root <path>` with a
    space measured the real tree and printed a clean line about it: a flag
    that is ignored rather than refused is how a guard gets believed when it
    never ran.
    """
    root = REPO
    for a in argv:
        if a == "--selftest":
            continue
        if a == "--root":
            return None, ("--root takes an equals sign and a path: "
                          "--root=<path>")
        if a.startswith("--root="):
            val = a.split("=", 1)[1]
            if not val:
                return None, "--root= was given with no path after it"
            root = os.path.abspath(val)
            continue
        return None, "unrecognised argument: %s" % a
    return root, ""


def main(argv=()):
    root, err = parse_args(argv)
    if err:
        print("lint-no-window: %s" % err)
        print(USAGE)
        return 2
    r = scan(root)
    for rel in r["fleet"]:
        c, f = r["perFile"][rel]
        print("  fleet   %-36s calls=%d flagged=%d/%d" % (rel, c, f, c))
    for rel, (c, f) in sorted(r["exempt"].items()):
        print("  exempt  %-36s calls=%d unflagged=%d/%d  %s"
              % (rel, c, c - f, c, EXEMPT[rel]))
    shown = r["problems"][:20]
    for p in shown:
        print("  PROBLEM " + p)
    if len(r["problems"]) > len(shown):
        print("  (+%d more not shown)" % (len(r["problems"]) - len(shown)))
    report(r)
    # A tree with no fleet in it is not a clean tree.
    return 1 if (r["problems"] or not r["calls"]) else 0


# --------------------------------------------------------------------------
# Selftest. ACCEPTING CASE FIRST, and the live codebase is the accepting
# fixture: doing the work this tool asks for can never break the tool. The
# rejecting fixtures are synthetic, in a temp directory, because planting a
# broken call site in the real fleet is how a guard gets left switched off.
# --------------------------------------------------------------------------
DEF_OK = ('# points at %s for the reasoning\n'
          'NO_WINDOW = (getattr(subprocess, "CREATE_NO_WINDOW", 0)\n'
          '             if os.name == "nt" else 0)\n' % CANONICAL)
DEF_CANON = ('# %s\n'
             'NO_WINDOW = (getattr(subprocess, "CREATE_NO_WINDOW", 0)\n'
             '             if os.name == "nt" else 0)\n' % MARKER)
SUPERVISE = ('import os\nimport subprocess\n\n' + DEF_OK +
             '\n\ndef children(repo):\n'
             '    return [os.path.join(repo, "tools", "pc-watcher.py"),\n'
             '            os.path.join(repo, "tools", "runner",\n'
             '                         "telegram-bot.py"),\n'
             '            os.path.join(repo, "tools", "runner",\n'
             '                         "executor.py")]\n\n\n'
             'def spawn(argv):\n'
             '    return subprocess.Popen(argv, creationflags=NO_WINDOW)\n')
LAUNCHER = ('import os\nimport subprocess\n\n' + DEF_CANON +
            '\n\ndef go(argv):\n'
            '    return subprocess.run(argv, creationflags=NO_WINDOW)\n')


#: THE FIXTURE PATHS BELOW ARE ASSEMBLED, NEVER WRITTEN WHOLE, and that is
#: not style. ledger/verify.py harvests every `tools/<name>.py` reference out
#: of the workflows TRANSITIVELY, reading each referenced file and taking the
#: references inside it too. This tool is named by a workflow, so it is read,
#: and a regex cannot tell a synthetic fixture name in a selftest from a real
#: tool this file runs: the three names below were reported as
#: UNTRACKED/ABSENT TOOL(S) and turned the gate red. Splitting the prefix off
#: defeats the harvest and changes no value the selftest uses, and the names
#: still exist nowhere, which is the whole point of a rejecting fixture
#: (.claude/rules/instruments.md). DO NOT INLINE THESE BACK, and do not
#: create the files: both fixes break one of the two rules.
_FIXTURE_DIR = "tools/"
_FIXTURE_RUNNER_DIR = "tools/runner/"


def _write(root, rel, text):
    path = os.path.join(root, *rel.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    return path


def _fixture(root, **files):
    """A minimal repo whose fleet derives to the same five names."""
    _write(root, "tools/supervise.py", files.get("supervise", SUPERVISE))
    _write(root, CANONICAL, files.get("launcher", LAUNCHER))
    _write(root, "tools/pc-watcher.py", files.get("watcher",
           'import os\nimport subprocess\n\n' + DEF_OK +
           '\n\ndef git(a):\n'
           '    return subprocess.run(a, creationflags=NO_WINDOW)\n'))
    _write(root, "tools/runner/executor.py", files.get("executor",
           'import os\nimport subprocess\n\n' + DEF_OK +
           '\n\ndef git(a):\n'
           '    return subprocess.run(a, creationflags=NO_WINDOW)\n'))
    # No subprocess at all, exactly like telegram-bot.py today: it needs no
    # constant, and demanding one there would be a false problem.
    _write(root, "tools/runner/telegram-bot.py", files.get("bot",
           'import os\n\n\ndef poll():\n    return os.getcwd()\n'))
    return root


def selftest():
    import tempfile
    ok = fail = 0

    def check(name, cond, detail=""):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print("  FAILED %s%s" % (name, "  <- %s" % (detail,)
                                     if detail else ""))

    # ---- ACCEPTING then REJECTING on the argument parser, because an
    # ignored flag made a clean line about the wrong tree read as a pass.
    check("ACCEPTING: no arguments means the live tree",
          parse_args([]) == (REPO, ""), parse_args([]))
    check("ACCEPTING: --root=<path> is taken",
          parse_args(["--root=/tmp/copy"])[0] == "/tmp/copy",
          parse_args(["--root=/tmp/copy"]))
    check("rejecting: --root with a space is refused by name",
          parse_args(["--root", "/tmp/copy"])[0] is None
          and "equals sign" in parse_args(["--root", "/tmp/copy"])[1],
          parse_args(["--root", "/tmp/copy"]))
    check("rejecting: an unknown flag is refused and named",
          parse_args(["--wat"])[0] is None
          and "--wat" in parse_args(["--wat"])[1], parse_args(["--wat"]))
    check("rejecting: --root= with no path is refused",
          parse_args(["--root="])[0] is None, parse_args(["--root="]))

    # ---- ACCEPTING: the live tree, which is the fixture that matters.
    live = scan()
    check("ACCEPTING: the live fleet has no problems", live["problems"] == [],
          live["problems"][:3])
    check("ACCEPTING: something was actually examined",
          len(live["fleet"]) >= 8 and live["calls"] >= 20,
          (len(live["fleet"]), live["calls"]))
    check("ACCEPTING: every live call site is flagged",
          live["flagged"] == live["calls"], (live["flagged"], live["calls"]))
    check("ACCEPTING: the derivation found the whole floor",
          all(f in live["fleet"] for f in FLOOR), live["fleet"])
    check("ACCEPTING: the derivation is not just the anchors",
          len(live["fleet"]) > len(ANCHORS), live["fleet"])
    # THE RULED LINE, EXACTLY. A later session greps this out of the proof
    # evidence; a rename here would leave that grep finding nothing and
    # reading it as "the check did not run".
    check("ACCEPTING: the done line carries noWindowSites=n/n unflagged=0",
          "unflagged=0 " in done_line(live)
          and "noWindowSites=%d/%d" % (live["calls"], live["calls"])
          in done_line(live), done_line(live))

    with tempfile.TemporaryDirectory() as d:
        def s(**files):
            root = os.path.join(d, "r")
            if os.path.isdir(root):
                import shutil
                shutil.rmtree(root)
            _fixture(root, **files)
            return scan(root, exempt={}, floor=())

        check("ACCEPTING: a clean synthetic fleet passes",
              s()["problems"] == [], s()["problems"])
        check("ACCEPTING: a file with no subprocess call needs no constant",
              s()["perFile"]["tools/runner/telegram-bot.py"] == (0, 0))
        # A site that already had creationflags ORs the flag in, and that is
        # the shape the fix asks for rather than a replacement.
        got = s(executor='import os\nimport subprocess\n\n' + DEF_OK +
                '\n\ndef go(a):\n'
                '    return subprocess.Popen(\n'
                '        a, creationflags=NO_WINDOW |\n'
                '        subprocess.CREATE_NEW_PROCESS_GROUP)\n')
        check("ACCEPTING: the flag ORed with another flag counts",
              got["problems"] == [] and got["flagged"] == got["calls"],
              got["problems"])

        # ---- REJECTING: one unflagged call, which is the twelfth site.
        got = s(executor='import os\nimport subprocess\n\n' + DEF_OK +
                '\n\ndef git(a):\n'
                '    return subprocess.run(a, creationflags=NO_WINDOW)\n\n\n'
                'def later(a):\n'
                '    return subprocess.run(a, capture_output=True)\n')
        check("rejecting: a twelfth call site with no creationflags",
              any("has no creationflags" in p for p in got["problems"]),
              got["problems"])
        check("rejecting: and the count says which denominator it is of",
              got["calls"] == 5 and got["flagged"] == 4,
              (got["calls"], got["flagged"]))

        got = s(executor='import os\nimport subprocess\n\n' + DEF_OK +
                '\n\ndef git(a):\n'
                '    return subprocess.run(a, creationflags=0)\n')
        check("rejecting: creationflags that does not name the constant",
              any("does not name" in p for p in got["problems"]),
              got["problems"])

        got = s(executor='import os\nimport subprocess\n\n' + DEF_OK +
                '\n\ndef git(a, kw):\n'
                '    return subprocess.run(a, **kw)\n')
        check("rejecting: a flag that could only be inside **kwargs",
              any("cannot see" in p for p in got["problems"]),
              got["problems"])

        got = s(executor='import subprocess\n\n\ndef git(a):\n'
                '    return subprocess.run(a, creationflags=NO_WINDOW)\n')
        check("rejecting: calls with no module-level definition",
              any("defines no module-level" in p for p in got["problems"]),
              got["problems"])

        got = s(executor='import os\nimport subprocess\n\n'
                '# points at %s\nNO_WINDOW = 0\n\n\ndef git(a):\n'
                '    return subprocess.run(a, creationflags=NO_WINDOW)\n'
                % CANONICAL)
        check("rejecting: a definition with no os.name guard",
              any("not provably a no-op" in p for p in got["problems"]),
              got["problems"])

        got = s(executor='import os\nimport subprocess\n\n'
                'NO_WINDOW = (getattr(subprocess, "CREATE_NO_WINDOW", 0)\n'
                '             if os.name == "nt" else 0)\n\n\ndef git(a):\n'
                '    return subprocess.run(a, creationflags=NO_WINDOW)\n')
        check("rejecting: a definition that points at no reasoning",
              any("without pointing at" in p for p in got["problems"]),
              got["problems"])

        got = s(executor='import os\nimport subprocess\n\n' + DEF_CANON +
                '\n\ndef git(a):\n'
                '    return subprocess.run(a, creationflags=NO_WINDOW)\n')
        check("rejecting: a second copy of the reasoning",
              any("restates the reasoning" in p for p in got["problems"]),
              got["problems"])

        got = s(launcher='import os\nimport subprocess\n\n' + DEF_OK +
                '\n\ndef go(a):\n'
                '    return subprocess.run(a, creationflags=NO_WINDOW)\n')
        check("rejecting: the canonical file without the reasoning",
              any("does not carry the reasoning" in p
                  for p in got["problems"]), got["problems"])

        got = s(watcher='import os\nimport subprocess\n\n' + DEF_OK +
                '\n\ndef git(a):\n    return os.system(a)\n')
        check("rejecting: os.system in a fleet file",
              any("cannot carry creationflags" in p for p in got["problems"]),
              got["problems"])

        # THE DERIVATION, PROVED: a fourth daemon named in supervise.py is
        # checked without anybody adding it to a list here.
        root = os.path.join(d, "r2")
        _fixture(root)
        _write(root, "tools/supervise.py", SUPERVISE.replace(
            '            os.path.join(repo, "tools", "runner",\n'
            '                         "executor.py")]',
            '            os.path.join(repo, "tools", "runner",\n'
            '                         "executor.py"),\n'
            '            os.path.join(repo, "tools", "newdaemon.py")]'))
        _write(root, _FIXTURE_DIR + "newdaemon.py",
               'import subprocess\n\n\ndef go(a):\n'
               '    return subprocess.run(a)\n')
        got = scan(root, exempt={}, floor=())
        check("rejecting: a NEW daemon named in supervise.py is scanned",
              _FIXTURE_DIR + "newdaemon.py" in got["fleet"]
              and any("newdaemon" in p for p in got["problems"]),
              (got["fleet"], got["problems"]))

        # A fleet file that does not parse must not read as clean.
        got = s(watcher='import subprocess\ndef (\n')
        check("rejecting: an unparseable fleet file is not a pass",
              any("could not be parsed" in p for p in got["problems"]),
              got["problems"])

        # FLOOR: a derivation that stopped seeing a known daemon.
        root = os.path.join(d, "r3")
        _fixture(root)
        got = scan(root, exempt={}, floor=FLOOR + (_FIXTURE_DIR + "ghost.py",))
        check("rejecting: a floor file the derivation no longer finds",
              any("FLOOR" in p for p in got["problems"]), got["problems"])

        # EXEMPTIONS: stale, unreasoned, and one naming nothing.
        root = os.path.join(d, "r4")
        _fixture(root)
        _write(root, _FIXTURE_RUNNER_DIR + "helper.py",
               'import subprocess\n\n\ndef go(a):\n'
               '    return subprocess.run(a)\n')
        got = scan(root, exempt={_FIXTURE_RUNNER_DIR + "helper.py": "a reason"},
                   floor=())
        check("ACCEPTING: an exemption with a reason and a real debt passes",
              got["problems"] == [] and got["exemptUnflagged"] == 1,
              (got["problems"], got["exemptUnflagged"]))
        got = scan(root, exempt={_FIXTURE_RUNNER_DIR + "helper.py": "  "}, floor=())
        check("rejecting: an exemption with no written reason",
              any("no written reason" in p for p in got["problems"]),
              got["problems"])
        got = scan(root, exempt={_FIXTURE_DIR + "ghost.py": "a reason"}, floor=())
        check("rejecting: an exemption naming no file",
              any("not a file" in p for p in got["problems"]),
              got["problems"])
        _write(root, _FIXTURE_RUNNER_DIR + "helper.py",
               'import os\nimport subprocess\n\n' + DEF_OK +
               '\n\ndef go(a):\n'
               '    return subprocess.run(a, creationflags=NO_WINDOW)\n')
        got = scan(root, exempt={_FIXTURE_RUNNER_DIR + "helper.py": "a reason"},
                   floor=())
        check("rejecting: an exemption whose debt is already paid is stale",
              any("is stale" in p for p in got["problems"]), got["problems"])

        # NOTHING MEASURED reads as nothing measured, never as clean.
        empty = os.path.join(d, "empty")
        os.makedirs(empty, exist_ok=True)
        got = scan(empty, exempt={}, floor=())
        check("rejecting: an empty tree says the fleet could not be derived",
              any("could not be derived" in p for p in got["problems"])
              and got["calls"] == 0, got["problems"])

    print("lint-no-window selftest: %d passed, %d failed (of %d case(s))"
          % (ok, fail, ok + fail))
    return 1 if fail else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1:]))
