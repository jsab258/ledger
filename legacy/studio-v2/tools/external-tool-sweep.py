#!/usr/bin/env python3
"""Every external binary a Python file shells out to, and whether a missing one
CRASHES the file or SKIPS a check.

    python3 tools/external-tool-sweep.py                 # sweep ledger/verify.py
    python3 tools/external-tool-sweep.py --selftest      # accepting case first
    python3 tools/external-tool-sweep.py --file X --via run

WHY THIS EXISTS, and it is not tidiness.

On 10 September `python3 ledger/verify.py` did not fail in this container: it
RAISED, out of `shape()`, the FIRST check in `main()`'s tuple.

    FileNotFoundError: [Errno 2] No such file or directory: 'dotnet'

So checksRun was 0, no check after it ever executed, and `ledger/.verify-footer`
was absent rather than red. The whole pre-commit gate was unreachable on any
container without the .NET SDK, which means a commit made from one cannot carry
a real footer at all. The file already knew the answer three times over, in
`ue-probe instruments SKIPPED (no g++ in this container)` and two siblings. But
a skip written per call site is the shape this project keeps paying for: one
idea, seventy sites, and the site nobody edited is the one that raises.

THE DENOMINATOR IS THE POINT. "verify.py handles missing tools" and "verify.py
handles the missing tool somebody remembered" are different facts, and only a
walk of every invocation can tell them apart. This tool is that walk, so the
claim has a number under it and keeps having one after the next call site lands.

WHAT IT COUNTS, and each is a statistic OF something named:

    callSites          cumulative: every subprocess invocation in the file
    binaries           distinct argv[0] values that are bare names (PATH lookup)
    resolveHere        of those binaries, how many `shutil.which` finds NOW
    guarded            call sites reaching the chokepoint (`run()` by default),
                       which is where the missing-tool check lives
    unguarded          call sites going straight to `subprocess.*`, which raise
    dynamic            call sites whose argv[0] is not a literal, reported and
                       not judged, since the sweep cannot know what they run

A CALL SITE WITH A PATH SEPARATOR IN argv[0] IS NOT AN EXTERNAL TOOL. It is a
file this repo built or ships (`str(binp)`, a compiled test binary), and a
missing one is a real failure rather than an absent container tool. Those are
counted separately and never drive the exit code, because turning them into
skips would hide exactly the build failure worth seeing.

EXIT CODES, distinct per outcome so a caller need not read prose:

    0   swept clean: no unguarded call site to a binary missing HERE
    1   a latent crash: unguarded call site whose binary does not resolve here
    2   NOTHING MEASURED: the file did not parse, or holds no call sites

`unguardedResolving` is PRINTED AND NOT FAILED: a direct `subprocess.run(["git",
...])` works in every container that has git and would crash one that does not.
That is a series to watch, not a bound anybody has measured. It is on the done
line so the next reader can set one from evidence.
"""
import argparse
import ast
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from capsay import cap as _cap, NOTHING_MEASURED   # noqa: E402

DEFAULT_FILE = ROOT / "ledger" / "verify.py"
DEFAULT_VIA = "run"

# The subprocess entry points that actually start a process. `subprocess.PIPE`
# and friends are attributes, not calls, and never appear here.
_SUBPROCESS_STARTERS = ("run", "Popen", "call", "check_call", "check_output")


class Site:
    """One subprocess invocation, with everything the report needs about it."""

    def __init__(self, line, argv0, kind, guarded, where):
        self.line = line              # 1-based line in the swept file
        self.argv0 = argv0            # literal name/path, or None when dynamic
        self.kind = kind              # "binary" | "path" | "dynamic"
        self.guarded = guarded        # reached the chokepoint rather than subprocess
        self.where = where            # enclosing def, or "<module>"


def _argv0(node):
    """argv[0] of a call whose first positional arg is a list literal.

    Returns (text, kind). `kind` is "binary" for a bare name that PATH resolves,
    "path" for anything holding a separator (a file this repo built), "dynamic"
    when the sweep cannot see the value.
    """
    if not node.args:
        return None, "dynamic"
    first = node.args[0]
    # `run(["python3", tool] + [str(r) for r in roots])` is a BinOp, not a list,
    # and reading it as dynamic UNDERCOUNTS the binary call sites. Measured: the
    # first draft of this file called 3 of verify.py's 86 sites dynamic on
    # exactly that shape, in `lint`, `ue_probe_tests` and `_git`. That is the
    # instrument reporting a smaller exposure than the file actually has. argv[0]
    # is always the leftmost operand of a chain of concatenations.
    while isinstance(first, ast.BinOp) and isinstance(first.op, ast.Add):
        first = first.left
    if not isinstance(first, (ast.List, ast.Tuple)) or not first.elts:
        return None, "dynamic"
    head = first.elts[0]
    if not isinstance(head, ast.Constant) or not isinstance(head.value, str):
        return None, "dynamic"
    text = head.value
    if os.sep in text or (os.altsep and os.altsep in text):
        return text, "path"
    return text, "binary"


def _chokepoint_guards(tree, via):
    """Does the wrapper named `via` ACTUALLY check for a missing tool.

    WITHOUT THIS THE SWEEP LIES BY ARITHMETIC. "guarded=70/72" reads as a
    reassurance, but routing seventy call sites through a wrapper that does not
    look is exactly the state that raised out of the first check on 10 September
    on 10 September, where the sites were all "guarded" by a chokepoint that
    guarded nothing. So the denominator is only allowed to count a site as
    guarded once the wrapper has been read and found to look.

    THE SIGNAL IS STRUCTURAL, not a name: the wrapper body must both consult
    PATH (a call to `which`) and `raise`, which together are the only shape that
    can turn an absent binary into something a caller may catch. A wrapper that
    calls `which` and returns quietly is not a guard, and neither is one that
    raises for some other reason.
    """
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.name != via:
            continue
        looks = raises = False
        for inner in ast.walk(node):
            if isinstance(inner, ast.Call):
                fn = inner.func
                name = fn.attr if isinstance(fn, ast.Attribute) else \
                    (fn.id if isinstance(fn, ast.Name) else "")
                if name == "which":
                    looks = True
            elif isinstance(inner, ast.Raise):
                raises = True
        return looks and raises
    return False


def sweep(path, via=DEFAULT_VIA):
    """Walk one Python file. Returns (sites, guards, error). `error` is a string
    when the file could not be read or parsed, in which case sites is empty and
    the caller must print NOTHING MEASURED rather than a clean zero. `guards`
    says whether the chokepoint itself looks for a missing tool."""
    try:
        src = pathlib.Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        return [], False, "%s: %s" % (type(exc).__name__, exc)
    try:
        tree = ast.parse(src)
    except SyntaxError as exc:
        return [], False, "SyntaxError line %s: %s" % (exc.lineno, exc.msg)
    guards = _chokepoint_guards(tree, via)

    # Enclosing def per line, so an unguarded site reports WHERE rather than
    # only a line number a reader then has to go and look up.
    owner = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            for ln in range(node.lineno, end + 1):
                # Innermost def wins: a nested helper is the truthful owner.
                prev = owner.get(ln)
                if prev is None or node.lineno > prev[0]:
                    owner[ln] = (node.lineno, node.name)

    sites = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn, guarded = node.func, None
        if isinstance(fn, ast.Attribute) and fn.attr in _SUBPROCESS_STARTERS \
                and isinstance(fn.value, ast.Name) and fn.value.id == "subprocess":
            guarded = False
        elif isinstance(fn, ast.Name) and fn.id == via:
            # A SITE IS ONLY GUARDED IF THE CHOKEPOINT LOOKS. Reaching a wrapper
            # that does not check PATH is the 10 September state exactly.
            guarded = guards
        if guarded is None:
            continue
        text, kind = _argv0(node)
        where = owner.get(node.lineno, (0, "<module>"))[1]
        # The chokepoint's own body calls subprocess; that one invocation IS the
        # guard, not a site the guard has missed.
        if where == via and not isinstance(fn, ast.Name):
            continue
        sites.append(Site(node.lineno, text, kind, guarded, where))
    return sites, guards, None


def report(path, via=DEFAULT_VIA, quiet=False):
    """Print the series, then the done line. Returns the exit code."""
    sites, guards, err = sweep(path, via)
    rel = str(pathlib.Path(path))
    if err is not None:
        print("external-tool-sweep: %s (%s): %s" % (NOTHING_MEASURED, rel, err))
        return 2
    if not sites:
        print("external-tool-sweep: %s (%s): 0 subprocess call site(s) found"
              % (NOTHING_MEASURED, rel))
        return 2

    binaries = {}
    for s in sites:
        if s.kind == "binary":
            binaries.setdefault(s.argv0, []).append(s)
    resolved = {b: shutil.which(b) for b in binaries}

    # PER-BINARY LINES ARE THE SAMPLE LINES: counts here are per binary, and
    # the whole-run totals are on the done line below. Sorted by call sites
    # descending so the biggest exposure reads first.
    paths = [s for s in sites if s.kind == "path"]
    dynamic = [s for s in sites if s.kind == "dynamic"]

    # NO SPACES IN A key=value VALUE, so the truncation announces itself as a
    # FRACTION rather than capsay's " (+N more of M)" clause: every reader of
    # these lines splits on whitespace, and a parenthetical would be dropped
    # silently, and a cap that does not say it bit reads as a finding. `_cap` still
    # owns the prose channels below, where spaces are safe.
    _SHOW = 3

    def _names(items):
        seen = sorted({i.where for i in items})
        return "/".join(seen[:_SHOW]) or "none", "%d/%d" % (min(_SHOW, len(seen)),
                                                            len(seen))

    if not quiet:
        for b in sorted(binaries, key=lambda k: (-len(binaries[k]), k)):
            hits = binaries[b]
            un = [h for h in hits if not h.guarded]
            names, shown = _names(un)
            print("  %-10s sites=%d guarded=%d unguarded=%d resolves=%s%s"
                  % (b, len(hits), len(hits) - len(un), len(un),
                     "yes" if resolved[b] else "NO",
                     ("  unguardedIn=%s unguardedInShown=%s" % (names, shown))
                     if un else ""))
        if dynamic:
            # argv[0] IS NOT A LITERAL HERE, so the sweep cannot say what runs.
            # Printed rather than folded into a total, because a count with no
            # way to go and look at it decays into a number nobody trusts.
            names, shown = _names(dynamic)
            # EVERY LINE, not the first three: this list is bounded by
            # dynamicSites on the done line and is the only handle a reader has
            # for going and looking, so a silent cap here would be the finding.
            print("  %-10s sites=%d argv0NotALiteral=%d inspectBy=hand "
                  "sitesIn=%s sitesInShown=%s lines=%s"
                  % ("<dynamic>", len(dynamic), len(dynamic), names, shown,
                     ",".join(str(d.line) for d in dynamic)))
    guarded = [s for s in sites if s.guarded]
    latent = [s for s in sites
              if s.kind == "binary" and not s.guarded and not resolved[s.argv0]]
    risky = [s for s in sites
             if s.kind == "binary" and not s.guarded and resolved[s.argv0]]

    # THE DONE LINE: whole-run, cumulative over the file. No spaces inside any
    # value, because this string is read out of logs by splitting readers.
    print("external-tool-sweep %s: callSites=%d binarySites=%d/pathSites=%d/"
          "dynamicSites=%d binaries=%d resolveHere=%d/%d chokepoint=%s()/%s "
          "guarded=%d/%d unguardedMissing=%d unguardedResolving=%d"
          % (rel, len(sites), len(sites) - len(paths) - len(dynamic), len(paths),
             len(dynamic), len(binaries), sum(1 for b in resolved if resolved[b]),
             len(binaries), via, "looks" if guards else "DOES-NOT-LOOK",
             len(guarded), len(sites), len(latent), len(risky)))

    if latent:
        print("LATENT CRASH: unguarded call site(s) to a binary missing here: "
              + _cap(["%s:%d %s in %s()" % (rel, s.line, s.argv0, s.where)
                      for s in latent], keep=3, width=70,
                     tail="nothing-measured"))
        return 1
    print("no unguarded call site to a missing binary (%d binary call site(s) "
          "examined, %d of %d binaries absent here)"
          % (len(sites) - len(paths) - len(dynamic),
             sum(1 for b in resolved if not resolved[b]), len(binaries)))
    return 0


# ------------------------------------------------------------------ selftest
# ACCEPTING CASE FIRST, and the accepting fixture is THE LIVE FILE: this tool
# checks the project itself, so `ledger/verify.py` as committed is what must
# sweep clean. The rejecting fixtures are synthetic and name a binary that
# exists NOWHERE, so doing the work this tool prompts can never break it.
#
# THE ACCEPTING ASSERTION DOES NOT DEPEND ON THIS CONTAINER'S PATH. It asserts
# "no unguarded site to a binary missing HERE", which holds on a machine with
# dotnet and on one without; asserting "dotnet is absent" would go red on
# Jafar's PC, which is the fixture-with-an-expiry-date fault.
_NOWHERE = "fnord-ledger-not-a-tool"      # deliberately unresolvable, everywhere

_REJECT_UNGUARDED = '''
import subprocess
def check():
    return subprocess.run(["%s", "--version"])
''' % _NOWHERE

_REJECT_EMPTY = '''
def check():
    return True, "nothing shells out here"
'''

# The chokepoint here LOOKS, meaning `which` plus `raise`, and that is the whole
# difference between this fixture and the rejecting one below. A first draft of
# this fixture omitted the guard and went red on its own accepting case, which
# is the sweep correctly refusing to call a wrapper that does not look a guard.
_ACCEPT_SYNTH = '''
import shutil, subprocess
def run(cmd):
    if shutil.which(cmd[0]) is None:
        raise RuntimeError(cmd[0])
    return subprocess.run(cmd)
def check():
    return run(["%s", "--version"])
''' % _NOWHERE


def _run_self(args):
    """This tool, as a subprocess, so the selftest reads the real exit code
    rather than a return value a refactor could stop propagating."""
    p = subprocess.run([sys.executable, str(pathlib.Path(__file__).resolve())]
                       + args, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def selftest():
    passed = failed = 0
    lines = []

    def say(ok, what, got):
        nonlocal passed, failed
        if ok:
            passed += 1
            lines.append("  ok   " + what)
        else:
            failed += 1
            lines.append("  FAIL %s: %s" % (what, got.strip().replace("\n", " | ")))

    # ---------------------------------------------------------- ACCEPTING
    code, out = _run_self(["--file", str(DEFAULT_FILE)])
    say(code == 0 and "unguardedMissing=0" in out and "callSites=" in out,
        "ACCEPTING: the live ledger/verify.py sweeps clean (exit 0)", out)

    say(code == 0 and "callSites=0" not in out and NOTHING_MEASURED not in out,
        "ACCEPTING: the live sweep measured something (callSites>0)", out)

    with tempfile.TemporaryDirectory() as td:
        acc = pathlib.Path(td) / "accept_via_chokepoint.py"
        acc.write_text(_ACCEPT_SYNTH, encoding="utf-8")
        code, out = _run_self(["--file", str(acc)])
        say(code == 0 and "unguardedMissing=0" in out and "guarded=1/1" in out,
            "ACCEPTING: a missing binary reached through the chokepoint is "
            "guarded, not a crash", out)

        # ---------------------------------------------------------- REJECTING
        rej = pathlib.Path(td) / "reject_unguarded.py"
        rej.write_text(_REJECT_UNGUARDED, encoding="utf-8")
        code, out = _run_self(["--file", str(rej)])
        say(code == 1 and "LATENT CRASH" in out and _NOWHERE in out,
            "REJECTING: an unguarded call to a binary that exists nowhere is "
            "exit 1 and names the binary", out)

        empty = pathlib.Path(td) / "reject_empty.py"
        empty.write_text(_REJECT_EMPTY, encoding="utf-8")
        code, out = _run_self(["--file", str(empty)])
        say(code == 2 and NOTHING_MEASURED in out,
            "REJECTING: a file with no call site prints nothing-measured and "
            "exits 2, never a clean zero", out)

        broken = pathlib.Path(td) / "reject_unparseable.py"
        broken.write_text("def check(:\n", encoding="utf-8")
        code, out = _run_self(["--file", str(broken)])
        say(code == 2 and NOTHING_MEASURED in out,
            "REJECTING: a file that will not parse is nothing-measured, not "
            "a clean sweep", out)

    return passed, failed, lines


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", default=str(DEFAULT_FILE),
                    help="Python file to sweep (default: ledger/verify.py)")
    ap.add_argument("--via", default=DEFAULT_VIA,
                    help="name of the guarded chokepoint wrapper (default: run)")
    ap.add_argument("--quiet", action="store_true",
                    help="done line only, no per-binary series")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    # FAIL READABLE. A report that ends in a BrokenPipeError traceback after a
    # correct run costs twenty minutes before somebody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass

    if args.selftest:
        passed, failed, lines = selftest()
        for l in lines:
            print(l)
        print("external-tool-sweep selftest: %d passed, %d failed (%d fixture(s), "
              "accepting and rejecting)" % (passed, failed, passed + failed))
        return 0 if failed == 0 else 1

    return report(args.file, args.via, args.quiet)


if __name__ == "__main__":
    sys.exit(main())
