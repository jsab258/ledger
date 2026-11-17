#!/usr/bin/env python3
"""Cap tool output carried into the conversation, without hiding any of it.

Efficiency item n16-10 (the advisor's review of 17 Nov 2026): helpers' shell
output and whole-file reads cost about US$67 in one day. This is one PreToolUse
hook for the session and every helper (settings-file hooks also fire inside
subagents; research: production/research/tool-tests-2026-11/
HOOK-OUTPUT-CAP-RESEARCH-2026-11-17.md). It dispatches on the tool:

Bash
  * Refuses, with a one-line hint, listings that walk a whole tree with no
    filter or count: `ls -R`, `find <dir>` without -name/-maxdepth/-mmin...,
    `tree` without -L, and `for f in <many>; do cat ...; done` with no
    head/grep/wc. Piping into head/tail/grep/wc/awk/sed (or a script), or
    redirecting to a file, counts as a filter.
  * Rewrites the command (updatedInput) so its stdout and stderr go to run
    files and only the head and tail come back (about 60 lines / 6,000
    characters in all), with the file's name and size. Output under the cap is
    printed whole and the run file deleted. The original command runs
    unchanged inside a `{ ...; }` group in the same shell, so cd, pipes, &&,
    heredocs and the exit code behave as before; the exit code of the group is
    returned unchanged.
  * Only rewrites in the auto and bypassPermissions modes: permission rules
    are matched against the rewritten text, so in other modes the project's
    allow rules (git add, dotnet test...) would start prompting.
  * Passes through untouched (and logs why): run_in_background calls, a
    trailing `&`, `exit`, `exec`, `set -e`, a heredoc without its closing
    line, a trailing backslash, and the opt-out marker `# full-output`.
PowerShell
  * Never rewritten (docs give no safe wrapper and $LASTEXITCODE semantics
    differ); only `Get-ChildItem -Recurse` with no filter/count is refused.
Read
  * A text file over 2,000 lines or 100 KB read with no offset/limit is refused
    with its outline (headings, def/class lines, with line numbers) and a
    request for a range. Images, PDFs and notebooks pass. `allow_large: true`
    is the explicit opt-out and is logged.

Run files: F:/LedgerTools/tmp/tool-output/<date>/ (storage map: working shelf;
retention.json scratch limit, age 7 days). Retention's deletion is still off
(17 Nov), so the hook removes its own date folders older than 7 days itself, at
most once a day (stamp file .pruned in that folder), only under
F:/LedgerTools/tmp/tool-output, each removal logged. Log of every wrap, refusal,
skip, opt-out and removal, key-like text redacted:
F:/LedgerTools/tmp/tool-output/log/<date>.tsv.

If F: has under 2 GB free the command runs unwrapped; if the run file cannot be
created when the command starts, the wrapper runs it plain. A shell that exits
inside the command (set -u, ${X:?}, a sourced exit, a TERM) still shows both
run files through an EXIT/TERM trap, with the exit code kept.

Any fault of the hook itself is swallowed (exit 0, no output): the tool call
then runs exactly as Claude wrote it. It must never stop the work.

Usage
  python tools/output_cap.py hook        (Claude Code runs this; JSON on stdin)
  python tools/output_cap.py --self-test (every case, real Git Bash runs)
"""
import datetime
import json
import os
import re
import secrets
import shutil
import subprocess
import sys

REAL_BASE = "F:/LedgerTools/tmp/tool-output"
BASE = os.environ.get("OUTPUT_CAP_DIR", REAL_BASE)
SHELF_ROOT = "F:/LedgerTools/tmp"          # must exist, or the hook stands aside
MIN_FREE = 2 * 1024 ** 3                   # below this on F:, run unwrapped
KEEP_DAYS = 7
OPT_OUT = "# full-output"
REWRITE_MODES = ("auto", "bypassPermissions")

# Display budget: shown whole when under these, else head + tail.
OUT_WHOLE_LINES, OUT_WHOLE_CHARS, OUT_HALF_LINES, OUT_HALF_CHARS = 60, 6000, 25, 2500
ERR_WHOLE_LINES, ERR_WHOLE_CHARS, ERR_HALF_LINES, ERR_HALF_CHARS = 12, 1500, 6, 600

READ_MAX_LINES, READ_MAX_BYTES = 2000, 100 * 1024
READ_PASS_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".pdf", ".ipynb"}
OUTLINE_MAX = 60

FILTER_WORDS = r"(head|tail|grep|egrep|fgrep|rg|wc|awk|gawk|sed|less|more|uniq|xargs|python3?|py|node|perl|jq|cut\s+-c)"


# --------------------------------------------------------------------------- log

def now():
    return datetime.datetime.now()


KEYLIKE = re.compile(
    r"sk-[A-Za-z0-9_-]{8,}|gh[pousr]_[A-Za-z0-9]{16,}|github_pat_\w+|xox[abpr]-[\w-]+|AKIA[0-9A-Z]{12,}"
    r"|(?:api[_-]?key|key|token|secret|password|passwd|authorization)\s*[=:]\s*(?:Bearer\s+|Basic\s+)?\S+"
    r"|Bearer\s+\S+", re.I)


def redact(text):
    return KEYLIKE.sub("[redacted]", text)


def log(event, data, detail):
    try:
        d = os.path.join(BASE, "log")
        os.makedirs(d, exist_ok=True)
        t = now()
        line = "\t".join([
            t.strftime("%Y-%m-%d %H:%M:%S"), event,
            str(data.get("agent_type") or "main"), str(data.get("tool_name", "")),
            redact(re.sub(r"\s+", " ", str(detail)))[:240],
        ])
        with open(os.path.join(d, t.strftime("%Y-%m-%d") + ".tsv"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def prune_base_allowed(base):
    """Only the real run folder, or a self-test sibling of it, is ever pruned."""
    b = os.path.normcase(os.path.abspath(base))
    real = os.path.normcase(os.path.abspath(REAL_BASE))
    return b == real or (os.path.dirname(b) == os.path.dirname(real)
                         and os.path.basename(b).startswith("tool-output-selftest-"))


def prune_runs(base=None, today=None):
    """Remove this hook's own date folders older than KEEP_DAYS, once a day.
    Returns the folders removed. Retention's deletion is still off (17 Nov)."""
    base = base or BASE
    today = today or now().date()
    removed = []
    if not prune_base_allowed(base) or not os.path.isdir(base):
        return removed
    stamp = os.path.join(base, ".pruned")
    try:
        if open(stamp, encoding="utf-8").read().strip() == today.isoformat():
            return removed
    except OSError:
        pass
    with open(stamp, "w", encoding="utf-8") as f:
        f.write(today.isoformat())
    for name in os.listdir(base):
        p = os.path.join(base, name)
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", name) or not os.path.isdir(p) or os.path.islink(p):
            continue
        try:
            day = datetime.date.fromisoformat(name)
        except ValueError:
            continue
        if (today - day).days > KEEP_DAYS:
            shutil.rmtree(p, ignore_errors=True)
            removed.append(p)
            log("pruned", {"tool_name": "-"}, "%s (own run files, older than %d days)" % (p, KEEP_DAYS))
    return removed


# --------------------------------------------------------------------- refusals

HEREDOC = re.compile(r"(?<!<)<<(-?)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")


def strip_heredocs(cmd):
    """The command with heredoc bodies removed: their text is data, not commands."""
    out, lines, i = [], cmd.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        i += 1
        for m in HEREDOC.finditer(line):
            dash, delim = m.group(1), m.group(3)
            while i < len(lines) and (lines[i].lstrip("\t") if dash else lines[i]).rstrip("\r") != delim:
                i += 1
            i += 1                                   # the closing line
    return "\n".join(out)


def segments(cmd):
    """Rough split into pipelines at ; && || and newlines (quotes not parsed:
    a wrong split can only miss a refusal or refuse a fragment, never run
    anything different)."""
    return [s.strip() for s in re.split(r"\n|;|&&|\|\|", cmd) if s.strip()]


def stages(seg):
    return [s.strip() for s in re.split(r"(?<!\|)\|(?!\|)", seg)]


def filtered(seg):
    """A later pipeline stage that reduces output, or a redirect to a file."""
    st = stages(seg)
    for later in st[1:]:
        if re.match(FILTER_WORDS + r"\b", later):
            return True
    if re.search(r"(?<![0-9&>])>{1,2}\s*[^&\s]", st[0]):
        return True
    return False


def first_word(stage):
    s = re.sub(r"^(\w+=\S*\s+)+", "", stage)       # leading VAR=value
    s = re.sub(r"^(sudo|command|time|nice)\s+", "", s)
    m = re.match(r"([^\s]+)", s)
    return (m.group(1) if m else ""), s


FIND_FILTERS = re.compile(
    r"\s-(i?name|i?path|wholename|i?regex|maxdepth|newer\w*|[acm]min|[acm]time|size|quit|delete|empty|links|samefile|inum"
    r"|exec|execdir|ok|okdir|print0|fprint\w*)\b")
QUOTED = re.compile(r"'[^']*'|\"(\\.|[^\"\\])*\"")


def blank_quotes(cmd):
    """Quoted text is data (a sed script, a grep pattern), never a command."""
    return QUOTED.sub("''", cmd)


def refuse_bash(cmd):
    """One-line hint when the command walks a whole tree unfiltered, else None."""
    cmd = blank_quotes(strip_heredocs(cmd))
    for seg in segments(cmd):
        st = stages(seg)
        word, rest = first_word(st[0])
        if word == "ls":
            args = rest.split()[1:]
            if any(re.match(r"^-[A-Za-z]*R", a) or a == "--recursive" for a in args) and not filtered(seg):
                return ("Refused: `ls -R` lists the whole tree. Use `find DIR -maxdepth 2 -name PATTERN`, "
                        "or pipe into `| head -50` / `| wc -l`; add `# full-output` if every line is needed.")
        if word == "find":
            if not FIND_FILTERS.search(rest) and not filtered(seg):
                return ("Refused: `find` with no -name/-path/-maxdepth/-mmin/-size and no `| head` or `| wc -l` "
                        "lists every file. Narrow it (e.g. `-maxdepth 2 -name '*.py'`) or count first; "
                        "add `# full-output` if every line is needed.")
        if word == "tree" and " -L" not in rest and not filtered(seg):
            return "Refused: `tree` with no -L walks everything. Use `tree -L 2` or `| head -50`; or `# full-output`."
    for m in re.finditer(r"\bfor\s+\w+\s+in\b(.*?)\bdo\b(.*?)\bdone\b([^\n;]*)", cmd, re.S):
        items, body, after = m.group(1), m.group(2), m.group(3)
        many = (bool(re.search(r"[*?\[]|\$\(|`", items)) or len(items.split()) > 5) \
            and not re.search(r"\|\s*head\b", items)
        cats = re.search(r"\bcat\b(?!\s*<<)(?!\s*>)", body)
        body_filter = re.search(r"\b(head|tail|grep|rg|wc|awk|sed\s+-n|cut|python3?)\b|>", body)
        after_filter = re.search(r"\|\s*" + FILTER_WORDS + r"\b", after) or re.search(r"(?<![0-9&>])>", after)
        if many and cats and not body_filter and not after_filter:
            return ("Refused: a loop that cats many files whole. Put `| head -n 40` (or grep/wc) inside the loop, "
                    "or after `done`; add `# full-output` if every line is needed.")
    return None


# Anchored to the start of a pipeline, so `$dir` or `Remove-Item ... -Recurse` never match.
PS_GCI = re.compile(r"(?:^|[;|\n({])\s*(Get-ChildItem|gci|dir|ls)\b([^|;\n}]*)", re.I)
PS_VALUE_PARAMS = {"-path", "-literalpath", "-lp", "-pspath", "-exclude", "-attributes", "-erroraction", "-ea",
                   "-filter", "-include", "-depth", "-outvariable", "-ov"}
PS_NOT_FILTER = re.compile(r"^(Sort-Object|sort|Format-\w+|ft|fl|fw|Out-String|Out-Host|oh)\b", re.I)


def ps_listing_filtered(args, later_stages):
    if re.search(r"\s-(Filter|Include|Depth)\b|\s>{1,2}\s*\S", " " + args, re.I):
        return True
    toks, positional, i = args.split(), [], 0
    while i < len(toks):
        t = toks[i]
        if t.startswith("-"):
            i += 2 if t.lower() in PS_VALUE_PARAMS else 1
            continue
        positional.append(t)
        i += 1
    if len(positional) >= 2 or any("*" in t or "?" in t for t in positional):
        return True                              # second positional is -Filter; a wildcard path filters
    return any(s.strip() and not PS_NOT_FILTER.match(s.strip()) for s in later_stages)


def refuse_powershell(cmd):
    cmd = blank_quotes(cmd)
    for m in PS_GCI.finditer(cmd):
        args = m.group(2)
        if not re.search(r"\s-(Recurse|r|s)\b", " " + args, re.I):
            continue
        line_rest = re.split(r"[;\n]", cmd[m.end(2):], 1)[0]
        later = line_rest.split("|")[1:]
        if not ps_listing_filtered(args, later):
            return ("Refused: `Get-ChildItem -Recurse` with no -Filter/-Include/-Depth and no `| Select-Object -First N` "
                    "or `| Measure-Object` lists the whole tree. Narrow or count it; add `# full-output` if every line is needed.")
    return None


# ---------------------------------------------------------------------- rewrite

def skip_reason(cmd):
    """Why a command is passed through untouched, or None to wrap it."""
    s = cmd.rstrip()
    if not s:
        return "empty"
    if s.endswith("\\"):
        return "trailing-backslash"
    plain = re.sub(r"'[^']*'|\"(\\.|[^\"\\])*\"", "''", strip_heredocs(s))
    if re.search(r"(^|[;&|({\s])(exit|exec)(\s|;|\)|$)", plain):
        return "exit-or-exec"
    if re.search(r"\bset\s+-[a-zA-Z]*e|\bset\s+-o\s+errexit|\bnohup\b|\bdisown\b", plain):
        return "errexit-or-detach"
    if re.search(r"(^|[;&|({\s])trap(\s|;|$)", plain):
        return "own-trap"
    if re.search(r"(?<![&|>])&(?![&>])", plain):
        return "background-ampersand"
    for m in re.finditer(r"(?<!<)<<(-?)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2", s):
        dash, delim = m.group(1), m.group(3)
        tail = s[m.end():].split("\n")[1:]
        if not any((ln.lstrip("\t") if dash else ln).rstrip("\r") == delim for ln in tail):
            return "heredoc-unterminated"
    return None


def shq(s):
    return "'" + s.replace("'", "'\\''") + "'"


def wrap(cmd, out_path, err_path):
    """The command inside a group in the same shell; head/tail display in sh."""
    show = (
        "__oc_show() { "
        "[ -s \"$1\" ] || { rm -f \"$1\"; return 0; }; "
        "__oc_l=$(wc -l < \"$1\"); __oc_c=$(wc -c < \"$1\"); "
        "if [ \"$__oc_l\" -le \"$2\" ] && [ \"$__oc_c\" -le \"$3\" ]; then cat \"$1\"; rm -f \"$1\"; return 0; fi; "
        "head -n \"$4\" \"$1\" | head -c \"$5\"; echo; "
        "echo \"[output-cap: $__oc_l lines, $__oc_c bytes in all; first and last $4 lines shown"
        " (at most $5 characters each); full output: $1 - Read it with offset/limit or grep it]\"; "
        "tail -n \"$4\" \"$1\" | tail -c \"$5\"; }; "
        "__oc_ret() { return \"$1\"; }; "
        # Shows both files once, to the saved original stdout/stderr (fds 7, 8):
        # when the shell exits inside the group its redirection is still active.
        "__oc_fin() { [ \"$__oc_done\" = 1 ] && return 0; __oc_done=1; "
        "__oc_show \"$__oc_o\" %d %d %d %d >&7; __oc_show \"$__oc_e\" %d %d %d %d >&8; }"
        % (OUT_WHOLE_LINES, OUT_WHOLE_CHARS, OUT_HALF_LINES, OUT_HALF_CHARS,
           ERR_WHOLE_LINES, ERR_WHOLE_CHARS, ERR_HALF_LINES, ERR_HALF_CHARS)
    )
    c = cmd.rstrip()
    return (
        "__oc_o=%s; __oc_e=%s; %s\n"
        "if mkdir -p \"${__oc_o%%/*}\" 2>/dev/null && : > \"$__oc_o\" 2>/dev/null && : > \"$__oc_e\" 2>/dev/null; then\n"
        "__oc_done=0; exec 7>&1 8>&2; __oc_old=$(trap -p EXIT TERM HUP INT); "
        "trap '__oc_x=$?; __oc_fin; exit $__oc_x' EXIT; trap '__oc_fin; exit 143' TERM; "
        "trap '__oc_fin; exit 129' HUP; trap '__oc_fin; exit 130' INT\n"
        "{ %s\n} > \"$__oc_o\" 2> \"$__oc_e\"; __oc_rc=$?; trap - EXIT TERM HUP INT; eval \"$__oc_old\"; "
        "__oc_fin; exec 7>&- 8>&-; __oc_ret $__oc_rc\n"
        "else\n{ %s\n}\nfi"
        % (shq(out_path), shq(err_path), show, c, c)
    )


def run_paths(data):
    t = now()
    d = os.path.join(BASE, t.strftime("%Y-%m-%d")).replace("\\", "/")
    os.makedirs(d, exist_ok=True)
    tag = re.sub(r"[^A-Za-z0-9]", "", str(data.get("tool_use_id", "")))[-8:] or secrets.token_hex(4)
    stem = "%s/%s-%s" % (d, t.strftime("%H%M%S"), tag)
    return stem + ".out", stem + ".err"


# ------------------------------------------------------------------------- read

OUTLINE_RES = {
    ".md": r"^#{1,6}\s+\S",
    ".py": r"^\s*(async\s+def|def|class)\s+\w",
    ".cs": r"^\s*(public|private|internal|protected|static|sealed|abstract|partial|namespace|class|struct|record|enum|interface)\b.*[\w>)]\s*(\{|$|\()",
    ".ts": r"^\s*(export\s+)?(async\s+)?(function|class|interface|enum|const\s+\w+\s*=\s*\()",
    ".js": r"^\s*(export\s+)?(async\s+)?(function|class|const\s+\w+\s*=\s*\()",
    ".ps1": r"^\s*(function|filter)\s+\S|^#\s*-{3,}|^#\s*={3,}",
    ".sh": r"^\s*(function\s+)?\w+\s*\(\)\s*\{|^#\s*-{3,}",
    ".json": r"^\s{0,2}\"[^\"]+\"\s*:",
    ".yaml": r"^[A-Za-z_][\w-]*:",
    ".yml": r"^[A-Za-z_][\w-]*:",
    ".toml": r"^\[",
    ".ini": r"^\[",
}
for _e in (".cpp", ".h", ".hpp", ".c"):
    OUTLINE_RES[_e] = r"^(class|struct|namespace|enum|U[A-Z]+\(|[A-Za-z_][\w:<>,\s\*&]*\s[\*&]?\w[\w:]*\s*\([^;]*$)"


def outline(path, ext):
    pat = re.compile(OUTLINE_RES.get(ext, r"^#{1,6}\s+\S|^\s*(def|class)\s+\w"))
    hits, n = [], 0
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, 1):
            if pat.search(line):
                hits.append("%6d  %s" % (n, line.rstrip()[:110]))
    if len(hits) > OUTLINE_MAX:
        step = len(hits) / OUTLINE_MAX
        hits = [hits[int(i * step)] for i in range(OUTLINE_MAX)] + ["   ... (%d outline lines in all, sampled evenly)" % len(hits)]
    return n, hits


def check_read(data):
    ti = data.get("tool_input") or {}
    path = ti.get("file_path") or ""
    if ti.get("offset") is not None or ti.get("limit") is not None or ti.get("pages"):
        return None
    ext = os.path.splitext(path)[1].lower()
    if ext in READ_PASS_EXT or not os.path.isfile(path):
        return None
    size = os.path.getsize(path)
    if ti.get("allow_large"):
        log("read-allow-large", data, "%s (%d bytes)" % (path, size))
        return None
    if size <= READ_MAX_BYTES:
        with open(path, "rb") as f:
            lines = sum(1 for _ in f)
        if lines <= READ_MAX_LINES:
            return None
    lines, hits = outline(path, ext)
    reason = ("Refused a whole read: %s has %d lines, %d KB (cap %d lines / %d KB). "
              "Read a range with offset and limit (up to 2,000 lines), Grep it for a term, "
              "or set allow_large to read it whole (logged).\nOutline (line number, text):\n%s"
              % (path, lines, size // 1024, READ_MAX_LINES, READ_MAX_BYTES // 1024,
                 "\n".join(hits) if hits else "   (no headings or definitions found)"))
    log("read-refused", data, "%s (%d lines, %d bytes)" % (path, lines, size))
    return reason


# ------------------------------------------------------------------------- hook

def deny(reason):
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                   "permissionDecision": "deny",
                                   "permissionDecisionReason": reason}}


def decide(data):
    """The hook's JSON reply for one PreToolUse input, or None for no change."""
    tool = data.get("tool_name")
    ti = data.get("tool_input") or {}
    if tool == "Read":
        r = check_read(data)
        return deny(r) if r else None
    if tool not in ("Bash", "PowerShell"):
        return None
    cmd = ti.get("command") or ""
    if OPT_OUT in cmd:
        log("opt-out", data, cmd)
        return None
    r = refuse_bash(cmd) if tool == "Bash" else refuse_powershell(cmd)
    if r:
        log("refused", data, cmd)
        return deny(r)
    if tool == "PowerShell":
        return None
    if ti.get("run_in_background"):
        log("skip:background-task", data, cmd)
        return None
    if data.get("permission_mode") not in REWRITE_MODES:
        log("skip:mode-%s" % data.get("permission_mode"), data, cmd)
        return None
    why = skip_reason(cmd)
    if why:
        log("skip:" + why, data, cmd)
        return None
    if not os.path.isdir(SHELF_ROOT):
        return None
    try:
        free = shutil.disk_usage(SHELF_ROOT).free
    except OSError:
        free = 0
    if free < MIN_FREE:
        log("skip:low-space", data, "%d MB free; %s" % (free // 2 ** 20, cmd))
        return None
    try:
        prune_runs()
    except Exception as e:
        log("prune-error", data, repr(e))
    out_p, err_p = run_paths(data)
    new = dict(ti)
    new["command"] = wrap(cmd, out_p, err_p)
    log("wrap", data, out_p.rsplit("/", 1)[-1] + " " + cmd)
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "updatedInput": new}}


def hook():
    try:
        data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace") or "{}")
        reply = decide(data)
        if reply:
            sys.stdout.write(json.dumps(reply))
    except Exception as e:                       # never stop the work
        try:
            log("hook-error", {}, repr(e))
        except Exception:
            pass
    return 0


# -------------------------------------------------------------------- self-test

def git_bash():
    for p in (r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files\Git\usr\bin\bash.exe"):
        if os.path.isfile(p):
            return p
    return shutil.which("bash")


def self_test():
    global BASE
    import tempfile
    base_parent = SHELF_ROOT if os.path.isdir(SHELF_ROOT) else tempfile.gettempdir()
    BASE = os.path.join(base_parent, "tool-output-selftest-" + secrets.token_hex(3)).replace("\\", "/")
    bash = git_bash()
    results = []

    def check(name, ok, info=""):
        results.append((name, bool(ok)))
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  -- " + info) if (info and not ok) else ""))

    def inp(cmd, tool="Bash", mode="auto", **extra):
        ti = {"command": cmd, "description": "t"}
        ti.update(extra)
        return {"tool_name": tool, "tool_input": ti, "permission_mode": mode,
                "tool_use_id": "toolu_" + secrets.token_hex(6), "agent_type": "self-test"}

    def sh(text, stdin=b""):
        p = subprocess.run([bash, "-c", text], capture_output=True, input=stdin)
        return p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace"), p.returncode

    def run(cmd, suffix="", stdin=b""):
        """Hook, then run what would run; (stdout, stderr, rc, reply)."""
        reply = decide(inp(cmd))
        final = reply["hookSpecificOutput"]["updatedInput"]["command"] if reply else cmd
        return sh(final + suffix, stdin) + (reply,)

    def run_files():
        out = []
        for root, _, files in os.walk(BASE):
            if os.path.basename(root) != "log":
                out += [os.path.join(root, f) for f in files if f.endswith((".out", ".err"))]
        return out

    try:
        # 1 small output: whole, identical, run files removed
        o, e, rc, rep = run("echo hello; echo world")
        check("small output shown whole", rep and o == "hello\nworld\n" and rc == 0, repr(o))
        check("small output leaves no run file", not run_files(), str(run_files()))
        # 2 big output capped, full file kept
        o, e, rc, _ = run("seq 1 100000")
        files = run_files()
        full = open(files[0], encoding="utf-8").read() if files else ""
        check("big output capped to ~6,000 chars", len(o) < 6500 and o.startswith("1\n") and o.rstrip().endswith("100000"), str(len(o)))
        check("cap names the run file and size", "[output-cap: 100000 lines" in o and ".out" in o, o[o.find("[output"):][:200])
        check("run file holds the full output", full.count("\n") == 100000, str(full.count("\n")))
        # 3 exit codes reach the caller unchanged
        check("exit code 0", run("true")[2] == 0)
        check("exit code 1 (false)", run("false")[2] == 1)
        check("exit code 7 from a child", run("bash -c 'seq 1 5000; exit 7'")[2] == 7)
        o, e, rc, _ = run("seq 1 100000 | grep -c 99999")
        check("pipe: last stage's code and output", rc == 0 and o.strip() == "1", repr(o))
        check("pipe: grep no-match code 1", run("echo a | grep zzz")[2] == 1)
        o, e, rc, _ = run("seq 1 3 && false && echo never")
        check("&& chain: code and output", rc == 1 and o == "1\n2\n3\n", repr(o))
        # 4 stderr stays on stderr, capped
        o, e, rc, _ = run("echo out; echo err >&2")
        check("stderr preserved on stderr", o == "out\n" and e == "err\n", repr((o, e)))
        o, e, rc, _ = run("seq 1 50000 >&2; bash -c 'exit 3'")
        check("big stderr capped on stderr, code 3", rc == 3 and len(e) < 2000 and "[output-cap: 50000 lines" in e and o == "", repr((rc, len(e))))
        # 5 heredoc with braces and $ inside
        cmd = "cat <<'EOF'\nline } with { and $HOME\n}\nEOF\necho after"
        o, e, rc, rep = run(cmd)
        check("heredoc: wrapped and exact", rep and o == "line } with { and $HOME\n}\nafter\n" and rc == 0, repr(o))
        o, e, rc, rep = run("python - <<'PY'\nimport sys\nprint(sum(range(10)))\nsys.exit(4)\nPY")
        check("heredoc into python: output and code 4", rep and o.strip() == "45" and rc == 4, repr((o, rc)))
        # 6 cd persists in the same shell; trailing comment
        o, e, rc, _ = run("cd / # go to root", suffix="\npwd")
        check("cd persists after the group", o.strip().endswith("/"), repr(o))
        # 7 quoting
        o, e, rc, _ = run("printf '%s\\n' \"a'b\" 'c\"d'")
        check("quotes untouched", o == "a'b\nc\"d\n", repr(o))
        # 8 long single line capped by characters
        o, e, rc, _ = run("python -c \"print('x'*300000)\"")
        check("one 300 KB line capped by chars", len(o) < 6500 and "[output-cap: 1 lines, 30000" in o, str(len(o)))
        o, e, rc, rep = run("python - <<'PY'\nimport subprocess\nx = 1 & 3\nprint(x)\nPY")
        check("heredoc body's & and exit words don't block the wrap", rep and o.strip() == "1", repr(o))
        # 9 pass-through cases
        for name, cmd in (("trailing &", "sleep 0 &"), ("exit", "echo a; exit 3"), ("exec", "exec echo a"),
                          ("set -e", "set -e; false"), ("unterminated heredoc", "cat <<EOF\nabc"),
                          ("trailing backslash", "echo a \\")):
            check("pass-through: " + name, decide(inp(cmd)) is None)
        check("pass-through: run_in_background", decide(inp("seq 1 9", run_in_background=True)) is None)
        check("pass-through: default mode (allow rules keep matching)", decide(inp("git status", mode="default")) is None)
        check("pass-through: dontAsk mode", decide(inp("git status", mode="dontAsk")) is None)
        check("rewrite: bypassPermissions mode", decide(inp("git status", mode="bypassPermissions")) is not None)
        rep = decide(inp("seq 1 100000 " + OPT_OUT))
        logs = open(os.path.join(BASE, "log", now().strftime("%Y-%m-%d") + ".tsv"), encoding="utf-8").read()
        check("opt-out marker passes untouched", rep is None)
        check("opt-out is logged", "\topt-out\t" in logs and "seq 1 100000" in logs)
        rep = decide(inp("git log", timeout=5000, dangerouslyDisableSandbox=False))
        ui = rep["hookSpecificOutput"]["updatedInput"] if rep else {}
        check("other tool_input fields kept", ui.get("timeout") == 5000 and "dangerouslyDisableSandbox" in ui and ui.get("description") == "t")
        check("no permissionDecision on a rewrite", rep and "permissionDecision" not in rep["hookSpecificOutput"])
        # 10 refusals
        refused = ["ls -R", "ls -laR /c/Users", "ls --recursive .", "find .", "find . -type f",
                   "cd x && find /f/LedgerTools", "tree", "for f in *.md; do cat \"$f\"; done",
                   "for f in $(find . -name '*.py'); do echo $f; cat $f; done"]
        allowed = ["ls -la", "ls -R | head -50", "ls -R > list.txt", "find . -name '*.py'", "find . -maxdepth 2",
                   "find . | wc -l", "find . -type f | grep foo", "find . -mmin -60", "find . -type f -exec grep -l x {} +",
                   "tree -L 2", "for f in *.md; do head -5 \"$f\"; done", "for f in *.md; do cat \"$f\"; done | wc -l",
                   "for f in a b; do cat $f; done", "cat <<EOF > x\nfind .\nEOF", "git log --oneline -5",
                   # review fix 4: the wrong refusals it found (2 from the replay, the rest constructed)
                   "sed -i 's#a; find more own leftovers ...#b#' production/handover/HANDOVER.md",
                   "grep -rn \"a; find .\" tools",
                   "for f in $(find . -name command.txt | head -5); do echo $f; cat $f; done",
                   "find tmp -type f -exec rm {} +", "find . -type f -print0 | xargs -0 rm -f",
                   "for f in *.txt; do cat \"$f\" >> \"$2\"; done"]
        for c in refused:
            r = decide(inp(c))
            check("refuse: " + c.replace("\n", " "), r and r["hookSpecificOutput"].get("permissionDecision") == "deny")
        for c in allowed:
            r = decide(inp(c))
            check("allow: " + c.replace("\n", " "), not (r and r["hookSpecificOutput"].get("permissionDecision") == "deny"))
        check("refusal hint is one line", "\n" not in decide(inp("ls -R"))["hookSpecificOutput"]["permissionDecisionReason"])
        check("refusals apply in default mode too", decide(inp("find .", mode="default")) is not None)
        # 11 PowerShell: never rewritten, recursive listing refused
        check("PowerShell untouched", decide(inp("Get-ChildItem C:\\x | Select-Object Name", tool="PowerShell")) is None)
        check("PowerShell long output untouched", decide(inp("Get-Content big.log", tool="PowerShell")) is None)
        r = decide(inp("Get-ChildItem -Recurse C:\\Users", tool="PowerShell"))
        check("PowerShell gci -Recurse refused", r and r["hookSpecificOutput"]["permissionDecision"] == "deny")
        for c in ("Remove-Item $dir -Recurse -Force", "Copy-Item $dir -Destination D:\\x -Recurse",
                  "Get-ChildItem . -Recurse -File | Remove-Item", "Get-ChildItem -Recurse *.cs",
                  "Get-ChildItem C:\\x *.log -Recurse", "Write-Host \"run dir -r later\""):
            check("PowerShell allow (review fix 4): " + c, decide(inp(c, tool="PowerShell")) is None)
        for c in ("Get-ChildItem -Recurse C:\\x | Sort-Object Length", "$x = 1; gci -r C:\\x",
                  "Get-ChildItem -Path C:\\x -Recurse | Format-Table"):
            r = decide(inp(c, tool="PowerShell"))
            check("PowerShell refuse: " + c, r and r["hookSpecificOutput"]["permissionDecision"] == "deny")
        for c in ("Get-ChildItem -Recurse -Filter *.py", "gci -r | Measure-Object", "Get-ChildItem -Recurse | Select-Object -First 20",
                  "Get-ChildItem -Recurse -Depth 2"):
            check("PowerShell allow: " + c, decide(inp(c, tool="PowerShell")) is None)
        # 12 Read
        d = os.path.join(BASE, "readtest")
        os.makedirs(d, exist_ok=True)
        big_md = os.path.join(d, "big.md")
        with open(big_md, "w", encoding="utf-8") as f:
            for i in range(3000):
                f.write(("## Section %d\n" % i) if i % 500 == 0 else "text line %d\n" % i)
        small = os.path.join(d, "small.py")
        with open(small, "w", encoding="utf-8") as f:
            f.write("def a():\n    pass\n")
        wide = os.path.join(d, "wide.py")
        with open(wide, "w", encoding="utf-8") as f:
            f.write("class Big:\n" + ("    x = '" + "y" * 200 + "'\n") * 600 + "def tail():\n    pass\n")
        rd = lambda p, **k: decide({"tool_name": "Read", "tool_input": dict(file_path=p, **k), "agent_type": "self-test"})
        r = rd(big_md)
        reason = r["hookSpecificOutput"]["permissionDecisionReason"] if r else ""
        check("Read: 3,000-line file refused", r and r["hookSpecificOutput"]["permissionDecision"] == "deny")
        check("Read: outline has headings with line numbers", "     1  ## Section 0" in reason and "  2501  ## Section 2500" in reason, reason[:300])
        check("Read: >100 KB short file refused with def/class outline", (lambda x: x and "class Big" in x["hookSpecificOutput"]["permissionDecisionReason"] and "def tail" in x["hookSpecificOutput"]["permissionDecisionReason"])(rd(wide)))
        check("Read: small file passes", rd(small) is None)
        check("Read: offset/limit passes", rd(big_md, offset=1, limit=2000) is None)
        check("Read: limit alone passes", rd(big_md, limit=50) is None)
        check("Read: allow_large passes", rd(big_md, allow_large=True) is None)
        logs = open(os.path.join(BASE, "log", now().strftime("%Y-%m-%d") + ".tsv"), encoding="utf-8").read()
        check("Read: allow_large logged", "read-allow-large" in logs)
        img = os.path.join(d, "pic.png")
        with open(img, "wb") as f:
            f.write(b"\x89PNG" + b"0" * 200000)
        check("Read: image passes", rd(img) is None)
        check("Read: missing file passes (tool reports it)", rd(os.path.join(d, "nope.txt")) is None)
        # 14 the review's inputs (17 Nov): plain and wrapped must give the same rc, stdout and stderr
        rv = os.path.join(BASE, "review").replace("\\", "/")
        os.makedirs(rv, exist_ok=True)
        exiter = rv + "/exits4.sh"
        with open(exiter, "w", encoding="utf-8", newline="\n") as f:
            f.write("echo inside\nexit 4\n")
        review_inputs = [
            ("cd \"/c/Program Files\" && pwd", b""),
            ("read x; echo \"got $x\"", b"hello\n"),
            ("printf '%s|%s\\n' \"a b\" 'c\"d'", b""),
            ("cat <<'EOF'\n{ } $HOME\nEOF", b""),
            ("if [ -d / ]; then echo yes; else echo no; fi", b""),
            ("false || echo recovered", b""),
            ("echo a # }", b""),
            ("echo a && echo b && false", b""),
            ("seq 1 5 | sort -r | head -2", b""),
            ("bash -c 'exit 9'", b""),
            ("echo out; echo err >&2; ls /nonexistent-oc", b""),
            ("echo start; set -u; echo $NOPE_UNSET; echo never", b""),
            ("echo start; : ${X_OC_UNSET:?missing X}; echo never", b""),
            ("echo before; source '%s'; echo after" % exiter, b""),
        ]
        for c, stdin in review_inputs:
            want = sh(c, stdin)
            o, e, rc, rep = run(c, stdin=stdin)
            same = rep is not None and (o, rc) == want[:1] + want[2:] and e.replace("bash: line 1: ", "").split(":")[-1] == want[1].replace("bash: line 1: ", "").split(":")[-1]
            check("review input same plain and wrapped: " + c.split("\n")[0][:50], same, repr(((o, e, rc), want)))
        o, e, rc, _ = run("echo start; set -u; echo $NOPE_UNSET")
        check("fix 1: set -u error shown, code kept", "start" in o and "unbound variable" in e and rc == sh("set -u; echo $NOPE_UNSET")[2], repr((o, e, rc)))
        o, e, rc, _ = run("echo before; source '%s'; echo after" % exiter)
        check("fix 1: sourced exit 4 shows its output, code 4", o == "before\ninside\n" and rc == 4, repr((o, rc)))
        o, e, rc, _ = run("echo before-term; kill -TERM $$; echo never")
        check("fix 1: TERM inside the group shows output, code 143", "before-term" in o and "never" not in o and rc == 143, repr((o, rc)))
        o, e, rc, _ = run("seq 1 100000; set -u; echo $NOPE_UNSET")
        check("fix 1: big output then early exit still capped with file name", "[output-cap: 100000 lines" in o and len(o) < 6500, str(len(o)))
        rep = decide(inp("echo hi"))
        o, e, rc = sh("trap 'echo old-trap' EXIT\n" + rep["hookSpecificOutput"]["updatedInput"]["command"])
        check("fix 1: a trap set before the wrapper is kept", o == "hi\nold-trap\n" and rc == 0, repr(o))
        check("fix 1: a command with its own trap passes through", decide(inp("trap 'rm -f x' EXIT; echo a")) is None)
        # fix 2: low space, folder gone, run file impossible
        global MIN_FREE
        saved = MIN_FREE
        MIN_FREE = 1 << 62
        check("fix 2: under 2 GB free -> run unwrapped", decide(inp("seq 1 100000")) is None)
        MIN_FREE = saved
        logs = open(os.path.join(BASE, "log", now().strftime("%Y-%m-%d") + ".tsv"), encoding="utf-8").read()
        check("fix 2: low space logged", "skip:low-space" in logs)
        rep = decide(inp("echo still-ran"))
        shutil.rmtree(os.path.join(BASE, now().strftime("%Y-%m-%d")), ignore_errors=True)
        o, e, rc = sh(rep["hookSpecificOutput"]["updatedInput"]["command"])
        check("fix 2: date folder deleted between hook and run -> command still runs", o == "still-ran\n" and rc == 0, repr((o, e)))
        blocker = rv + "/a-file"
        open(blocker, "w").close()
        o, e, rc = sh(wrap("echo plain-run; false", blocker + "/x.out", blocker + "/x.err"))
        check("fix 2: run file cannot be created -> plain run, code kept", o == "plain-run\n" and rc == 1, repr((o, e, rc)))
        # fix 3: the snippet can never exit 2
        snip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "production", "research", "tool-tests-2026-11", "HOOK-OUTPUT-CAP-SETTINGS.json")
        try:
            hcmd = json.load(open(snip, encoding="utf-8"))["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        except Exception:
            hcmd = ""
        check("fix 3: snippet command ends in '|| true'", hcmd.rstrip().endswith("|| true"), hcmd)
        o, e, rc = sh(hcmd.replace("$CLAUDE_PROJECT_DIR/tools/output_cap.py", rv + "/missing.py"), b"{}")
        check("fix 3: missing script -> exit 0, not 2", rc == 0, str(rc))
        # fix 8: key-like text never reaches the log
        decide(inp("curl -H 'Authorization: Bearer abc123secretvalue' https://example.invalid; "
                   "echo sk-ant-abcdefghijkl1234; X=1 token=zzzsecret ghp_abcdefghijklmnopqrstu"))
        logs = open(os.path.join(BASE, "log", now().strftime("%Y-%m-%d") + ".tsv"), encoding="utf-8").read()
        check("fix 8: log redacts keys", "[redacted]" in logs and not any(
            s in logs for s in ("abc123secretvalue", "sk-ant-abcdefghijkl1234", "zzzsecret", "ghp_abcdefghijklmnopqrstu")))
        # fix 9: the hook prunes its own date folders, once a day, only in its own folder
        today = now().date()
        old = os.path.join(BASE, (today - datetime.timedelta(days=10)).isoformat())
        recent = os.path.join(BASE, (today - datetime.timedelta(days=3)).isoformat())
        other = os.path.join(BASE, "not-a-date")
        for p in (old, recent, other):
            os.makedirs(p, exist_ok=True)
        try:
            os.remove(os.path.join(BASE, ".pruned"))
        except OSError:
            pass
        removed = prune_runs(BASE, today)
        check("fix 9: date folder older than 7 days removed", removed == [old] and not os.path.exists(old), str(removed))
        check("fix 9: recent and non-date folders kept", os.path.isdir(recent) and os.path.isdir(other))
        os.makedirs(old, exist_ok=True)
        check("fix 9: at most once a day", prune_runs(BASE, today) == [] and os.path.isdir(old))
        logs = open(os.path.join(BASE, "log", now().strftime("%Y-%m-%d") + ".tsv"), encoding="utf-8").read()
        check("fix 9: removal logged", "\tpruned\t" in logs)
        check("fix 9: never outside its own folder", not prune_base_allowed("F:/LedgerTools/tmp")
              and not prune_base_allowed("F:/LedgerTools") and not prune_base_allowed("C:/Users/Jafar/ledger-local")
              and prune_base_allowed(REAL_BASE) and prune_runs("F:/LedgerTools/tmp", today) == [])
        # 13 the hook entry point: JSON in, JSON out, faults swallowed
        p = subprocess.run([sys.executable, os.path.abspath(__file__), "hook"], input=json.dumps(inp("ls -R")).encode(),
                           capture_output=True, env=dict(os.environ, OUTPUT_CAP_DIR=BASE))
        check("hook entry: deny JSON on stdout, exit 0", p.returncode == 0 and json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny")
        p = subprocess.run([sys.executable, os.path.abspath(__file__), "hook"], input=b"not json", capture_output=True,
                           env=dict(os.environ, OUTPUT_CAP_DIR=BASE))
        check("hook entry: bad input -> exit 0, no output", p.returncode == 0 and p.stdout == b"")
        p = subprocess.run([sys.executable, os.path.abspath(__file__), "hook"],
                           input=json.dumps({"tool_name": "Grep", "tool_input": {"pattern": "x"}}).encode(), capture_output=True)
        check("hook entry: other tools untouched", p.returncode == 0 and p.stdout == b"")
    finally:
        shutil.rmtree(BASE, ignore_errors=True)
    failed = [n for n, ok in results if not ok]
    print("\n%d checks, %d passed, failed=%s" % (len(results), len(results) - len(failed), ", ".join(failed) or "none"))
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "hook":
        sys.exit(hook())
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        sys.exit(self_test())
    print(__doc__.strip().splitlines()[0] + "\nUsage: output_cap.py hook | --self-test")
    sys.exit(0)
