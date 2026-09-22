#!/usr/bin/env python3
"""WHAT A SPAWN COST, PER TIER AND PER TURN, INSTEAD OF PER SPAWN.

    python3 tools/spawn-cost.py --report              # read the turns log
    python3 tools/spawn-cost.py --transcripts DIR     # the series, from disk
    python3 tools/spawn-cost.py --work-split          # queue 370: what each
    python3 tools/spawn-cost.py --work-split --transcripts DIR   # session WROTE
    python3 tools/spawn-cost.py --hook                # SubagentStop, stdin JSON
    python3 tools/spawn-cost.py --selftest            # accepting case FIRST

WHY IT EXISTS. Every estimate in this project rests on "a spawn costs 1.5 to 2
points", which averages a 12-turn fable median with a 45-turn opus median
(transcripts on the build machine, 2026-09-03)
and is why the estimates here are consistently low. `.claude/agent-log.tsv`
records one row per spawn and nothing else, so the average is the only
statistic it can support. Jafar asked on 2026-09-03 for model tier and turn
count at SubagentStop, "so calibration is per tier and turns rather than per
spawn".

WHAT SubagentStop CAN ACTUALLY SEE, established from files rather than
assumed, because inventing a field the hook cannot fill is the silent failure
this whole tool is aimed at. The event and its payload are defined in the
Claude Code binary at /opt/claude-code/bin/claude:

    hook_event_name  "SubagentStop"
    stop_hook_active  agent_id  agent_transcript_path  agent_type
    last_assistant_message (optional)   background_tasks (optional)
    ... plus the common fields: session_id, transcript_path, cwd,
    prompt_id, permission_mode, effort

THERE IS NO MODEL FIELD AND NO TURN COUNT FIELD. Both are DERIVED, and from
the one field that makes deriving them possible: `agent_transcript_path`. The
subagent's own transcript is JSONL, one object per line, and every assistant
line carries `message.model` and `message.id`. So:

    tier   = the model family of the MODAL assistant message (most lines),
             mapped opus / fable / sonnet. Marked `+mixed` when more than one
             family appears, because a fallback mid-run is a different animal
             from a clean run and must not average silently into either.
    turns  = COUNT of DISTINCT `message.id` among assistant lines. One API
             assistant message is written to the transcript as several lines
             when it carries thinking, text and a tool call, so the line count
             runs about 1.8x the turn count here. Both are recorded: `turns`
             is what `maxTurns` bounds, `alines` is what anybody grepping the
             transcript will count, and a reader who confuses them is off by
             most of a factor of two.

THE TIER AND THE TURNS ARE READ AT THE SAME INSTANT, off one read of one file
at the moment the subagent stopped. The transcripts live under ~/.claude and
do not survive the container; the row in the repository does.

    wrote  the repo AREAS the session CHANGED, as area:writeCalls, from the
           tool_use blocks in that same transcript, off that same read, at
           that same instant. Queue 370, Jafar 2026-09-16: "The split cannot
           be computed at all until the spawn log records what a session
           touched, not just who ran and why." NOT SELF-REPORTED: a column an
           agent fills in about itself is an attendance register with an extra
           field, which is the fault being fixed, one layer along.
    fileToolsOfAll  its denominator, same instant: file-path tool calls out of
           ALL tool calls. `no-file-write 0/60` is a session that did sixty
           things through the shell; `no-file-write 0/0` is a session that did
           nothing, and the pair is the only thing that tells them apart.

WHAT THE COLUMN CANNOT ANSWER, COUNTED AND NEVER GUESSED. 4,178 of 8,069 tool
calls across the 130 live transcripts are Bash, whose `command` is a shell
string, not a path field. A redirection-target regex was written and MEASURED
before being rejected: 326 of the 348 in-repo "paths" it recovered were
fragments of Python heredocs, a 6% precision. So a shell write is not
recoverable, a session with none records the words, and every reading prints
the rows it could not answer for beside the rows it could. 325 rows on this
machine predate the column and read `pre-column` for ever: nothing rewrites a
row, and the transcripts behind them went with their containers.

AND THE SPLIT CARRIES A SECOND DENOMINATOR, because the four buckets above
are buckets of STOP-log rows and queue 370's sentence names the SPAWN log. A
spawn that never reached SubagentStop wrote no row here at all: it is in no
bucket, on no side, and invisible to `sessions=`. `--work-split` therefore
prints the spawn census beside its own reading, both directions
(`spawnIdsWithNoStopRow`, `stopIdsWithNoSpawnRow`), and splits the second at
the first id the spawn log ever carried, so a structural gap that can only
hold still cannot be read as a hook failing now. Measured 2026-09-21:
747 spawn rows, 217 carrying an id, 145 distinct ids, 11 with no stop row,
and 163 of this file's 297 sessions predating the id column entirely.

EXIT CODES, distinct per outcome. 0 a reading was printed. 1 the log or the
directory could not be read. 2 nothing measured: no rows, no transcripts, or
(--work-split) a session set whose `wrote` column answered for nobody, which
is a rung printed and not a split computed. 3 the selftest failed. The --hook mode ALWAYS exits 0: a broken audit trail
must never be able to stop the work it only describes.
"""
import argparse
import datetime
import json
import os
import pathlib
import re
import statistics
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent

# ONE IMPLEMENTATION PER IDEA: the truncation notice and the never-measured
# words already exist in this repo and are imported, never re-typed.
sys.path.insert(0, str(HERE))
from capsay import cap, NOTHING_MEASURED                          # noqa: E402

TURNS_LOG = ".claude/agent-turns.tsv"
# COLUMNS 7 AND 8 ADDED 2026-09-21 for queue 370. The first six are the
# shape every row written before that date carries; `LEGACY_COLUMNS` is that
# prefix BY NAME so a pre-370 row is read as a row that PREDATES the column
# rather than as a malformed one (see `read_log`). A row is never rewritten
# to acquire them: 325 rows on this machine can never answer, permanently,
# and a reader that let them vanish from a denominator would be the exact
# fault queue 370 exists to fix one layer along.
COLUMNS = ("when", "agent", "tier", "turns", "alines", "agentId",
           "wrote", "fileToolsOfAll")
LEGACY_COLUMNS = COLUMNS[:6]

# WHAT A SESSION TOUCHED, DERIVED AND NEVER SELF-REPORTED (queue 370).
#
# THE FAULT. `.claude/agent-log.tsv` names WHO ran, so every studio-versus-game
# reading is a count of ROLE NAMES: an engine-specialist repairing an
# instrument counts as game work and an instrument-builder adding a gameplay
# readback does not. Jafar, 2026-09-16: "Add the column before claiming the
# ratio again, or stop printing the number." The ratio is withdrawn; this is
# the column.
#
# WHO FILLS IT, which is the hard half. NOT the agent. The same transcript
# `read_transcript` already opens at SubagentStop to derive tier and turns
# carries every tool call the session made, so the areas it WROTE TO come off
# the same single read of the same file at the same instant. An agent that
# lied about its own work would have to lie in its tool calls.
#
# WRITES, NOT READS, AND THE MEASUREMENT SAYS WHY. Over the 130 subagent
# transcripts on this machine (2026-09-21): write paths per session median 1,
# peak 9; read paths per session median 5, peak 66, and 56 of 130 sessions
# read in more than four areas because every session opens CLAUDE.md, canon.md
# and the queue before it does anything. A split built on reads would put
# every session in every area. `wrote` is named for the statistic it is: the
# areas a session CHANGED.
#
# AND WHAT DEFEATS IT, MEASURED RATHER THAN ASSUMED. 4,178 of 8,069 tool calls
# in those transcripts are Bash, whose `command` is a shell string and not a
# path field. A regex that pulls redirection targets out of those strings was
# written and MEASURED before being rejected: of 348 distinct in-repo "write
# targets" it recovered, 326 do not exist and are fragments of Python heredocs
# (`assert s.count(old) == 1`, `new = """...`), a 6% precision that would have
# injected 326 phantom paths into this instrument. So a shell write is NOT
# recoverable here and is not guessed at: a session with no file-tool write
# records the words, and `fileToolsOfAll` ships the denominator beside them so
# "wrote nothing" can be told from "worked entirely through the shell".
AREA_DEPTH = 2              # ledger/Assets, tools/runner, production/queue
# AREAS_KEPT = 8 IS SET FROM THE SERIES THIS TOOL PRINTED, not before it. The
# first run over the 130 live transcripts with keep=4 reported "the per-row cap
# BIT: +5 area(s) carrying 8 write call(s)", and the distinct-write-area
# distribution behind it is median 1, peak 7, with 3 of 130 sessions above 4.
# A cap below the observed peak bites on ORDINARY sessions, and because a
# hidden area is counted in no side, a biting cap can silently move a session
# from `both` to `studio`. 8 clears the measured peak by one and still bounds
# the cell at roughly 240 characters. The announcement stays either way.
AREAS_KEPT = 8              # per row; the rest collapse into +Nmore:K
WROTE_NONE = "no-file-write"     # tool calls seen, none of them a file write
WROTE_NO_TOOLS = "no-tool-call"  # a spawn that called nothing at all
PRE_COLUMN = "pre-column"        # the row predates 2026-09-21; unanswerable
# The tool names whose input carries a LITERAL path field. Read off the 130
# live transcripts rather than from memory: Bash/Grep/Glob/WebFetch/WebSearch/
# SubagentHandback were the only other names present, and none of the first
# three names a file it CHANGED.
WRITE_TOOLS = ("Edit", "Write", "NotebookEdit", "MultiEdit")
WRITE_PATH_KEYS = ("file_path", "notebook_path")

# THE TIERS THIS STUDIO DECLARES, read off `.claude/agents/*.md` on
# 2026-09-03: 11 agents on opus, 2 on fable, 1 on sonnet. A tier in this list
# with no rows prints the words "nothing measured" rather than 0, because a
# tier nobody has spawned and a tier that ran 0 turns are different facts.
KNOWN_TIERS = ("opus", "fable", "sonnet")
TIER_OF = {"opus": "opus", "fable": "fable", "sonnet": "sonnet",
           "haiku": "haiku"}
# Claude Code writes `<synthetic>` as the model of a message it generated
# itself (an interrupt notice, a refusal). It is not a tier and its lines are
# not turns; a spawn whose transcript is nothing but synthetic lines produced
# NOTHING, and must not read as a one-turn opus spawn.
SYNTHETIC = "<synthetic>"
NO_TIER = "no-model"


def tier_of_model(model):
    """The tier a model name belongs to. Unknown names keep their own name
    rather than being bucketed into a tier they were never in."""
    if not model or model == SYNTHETIC:
        return None
    low = model.lower()
    for key, tier in TIER_OF.items():
        if key in low:
            return tier
    return "other:" + low.replace(" ", "-")


def rel_area(path, root=None):
    """One literal tool-call path -> the repo-relative AREA it sits in, or
    None when it is outside the repository.

    THE AREA IS THE DIRECTORY, capped at `AREA_DEPTH` segments, never the
    file. Measured reason: a decision record's own name is 96 characters and
    `game-design/decision-2026-09-14-ruling-the-prune-is-gone-...md` as an
    "area" would blow the column open one row at a time. A directory is also
    the thing a split is actually about.

    `ledger/verify.py` -> `ledger` and `ledger/Assets/Scripts/X.cs` ->
    `ledger/Assets`, which is the one boundary this project's own
    `DIRECTOR_WORK` table draws by hand: what is left of `ledger/` after the
    game project is carved out is the studio's checkers."""
    p = (path or "").strip()
    if not p:
        return None
    if p.startswith("~"):
        p = os.path.expanduser(p)
    base = str(pathlib.Path(root or REPO).resolve())
    full = os.path.normpath(p if os.path.isabs(p) else os.path.join(base, p))
    if full != base and not full.startswith(base + os.sep):
        return None                       # OUTSIDE THE REPO: counted, not area
    rel = os.path.relpath(full, base)
    parts = [x for x in rel.split(os.sep) if x not in ("", ".")]
    # THE FILENAME IS DROPPED FIRST, then the directory is capped. The first
    # draft of this function capped the FULL path instead, and the live series
    # it printed carried
    # `game-design/decision-2026-09-14-ruling-the-prune-is-gone-...md` as an
    # "area": a 96-character cell, one row at a time, and 68 areas where the
    # directories number far fewer.
    parts = parts[:-1]
    if not parts:
        return "."                        # a file at the repository root
    return "/".join(parts[:AREA_DEPTH])


def encode_touched(counter, keep=AREAS_KEPT):
    """{area: writeCalls} -> the column value. CUMULATIVE write CALLS per
    area, not distinct files: two edits to one file are two calls.

    NO SPACES, because every reader of a key=value or tab channel in this
    project splits on whitespace. THE CAP ANNOUNCES ITSELF in the value
    itself, carrying both how many areas it ate and how many calls went with
    them, so a truncated cell can never read as a complete one."""
    if not counter:
        return WROTE_NONE
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    top, rest = items[:keep], items[keep:]
    v = ",".join("%s:%d" % (a, n) for a, n in top)
    if rest:
        v += ",+%dmore:%d" % (len(rest), sum(n for _, n in rest))
    return v


def decode_touched(value):
    """The column value -> ({area: writeCalls}, hiddenAreas, hiddenCalls).

    A value that is one of the three sentinels decodes to an EMPTY map and is
    the caller's job to bucket: `{}` from `no-file-write` and `{}` from
    `pre-column` are the same shape and must never be the same fact."""
    areas, hidden_a, hidden_c = {}, 0, 0
    v = (value or "").strip()
    if not v or v in (WROTE_NONE, WROTE_NO_TOOLS, PRE_COLUMN, NOTHING_MEASURED):
        return areas, hidden_a, hidden_c
    for entry in v.split(","):
        if ":" not in entry:
            continue
        name, _, num = entry.rpartition(":")
        try:
            n = int(num)
        except ValueError:
            continue
        if name.startswith("+") and name.endswith("more"):
            try:
                hidden_a += int(name[1:-4])
            except ValueError:
                hidden_a += 1
            hidden_c += n
            continue
        areas[name] = areas.get(name, 0) + n
    return areas, hidden_a, hidden_c


def read_transcript(path, root=None):
    """One transcript, at one instant. Returns the whole reading as a dict.

    PURE ARITHMETIC IN THE TESTED LAYER: the hook shim below calls this and
    formats nothing itself, so nothing that computes a number here ships
    unrun.
    """
    r = {"turns": 0, "alines": 0, "tier": NO_TIER, "families": {},
         "unparsed": 0, "lines": 0, "synthetic": 0, "path": str(path),
         "synth_text": "",
         # QUEUE 370, off the SAME read at the SAME instant as tier and turns.
         "wrote": {}, "toolCalls": 0, "fileTools": 0, "bashCalls": 0,
         "outsideRepo": 0, "wroteValue": WROTE_NO_TOOLS,
         "fileToolsValue": "0/0"}
    ids = set()
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        r["tier"] = NOTHING_MEASURED
        # A TRANSCRIPT THAT IS NOT THERE MEASURED NOTHING, and must not read
        # as a session that wrote nothing: those are two different facts.
        r["wroteValue"] = NOTHING_MEASURED
        r["fileToolsValue"] = NOTHING_MEASURED
        return r
    for line in text.splitlines():
        if not line.strip():
            continue
        r["lines"] += 1
        try:
            d = json.loads(line)
        except ValueError:
            r["unparsed"] += 1          # COUNTED, never silently dropped
            continue
        if d.get("type") != "assistant":
            continue
        m = d.get("message") or {}
        model = m.get("model")
        if model == SYNTHETIC:
            r["synthetic"] += 1
            # WHY A SPAWN PRODUCED NOTHING IS THE HALF THAT MATTERS. 149 of
            # the 453 subagent transcripts on this machine hold exactly one
            # synthetic line reading "You've hit your session limit", which is
            # a spawn that was started, cost a slot, and did no work. Counted
            # as a 0-turn spawn with no reason it reads as a quiet agent.
            if not r["synth_text"]:
                c = m.get("content")
                if isinstance(c, list):
                    c = " ".join(str(b.get("text", "")) for b in c
                                 if isinstance(b, dict))
                r["synth_text"] = str(c or "")[:70].replace("\n", " ")
            continue
        r["alines"] += 1
        if m.get("id"):
            ids.add(m["id"])
        fam = tier_of_model(model)
        if fam:
            r["families"][fam] = r["families"].get(fam, 0) + 1
        # THE TOOL CALLS, in the same pass over the same bytes.
        content = m.get("content")
        if isinstance(content, list):
            for blk in content:
                if not (isinstance(blk, dict)
                        and blk.get("type") == "tool_use"):
                    continue
                r["toolCalls"] += 1
                name = blk.get("name")
                inp = blk.get("input")
                if not isinstance(inp, dict):
                    inp = {}
                if name == "Bash":
                    r["bashCalls"] += 1
                    continue
                if name not in WRITE_TOOLS:
                    continue
                r["fileTools"] += 1
                raw = ""
                for k in WRITE_PATH_KEYS:
                    if inp.get(k):
                        raw = inp[k]
                        break
                area = rel_area(raw, root)
                if area is None:
                    r["outsideRepo"] += 1   # COUNTED, never an invented area
                    continue
                r["wrote"][area] = r["wrote"].get(area, 0) + 1
    # turns = distinct API assistant messages. An assistant line with no
    # message.id (older transcripts) still counts as a turn of its own, or a
    # whole run of them would collapse to 0.
    r["turns"] = len(ids) if ids else r["alines"]
    if r["families"]:
        modal = max(r["families"].items(), key=lambda kv: kv[1])[0]
        r["tier"] = modal + ("+mixed" if len(r["families"]) > 1 else "")
    # THE THREE STATES A ZERO WOULD MERGE. A session that called no tool at
    # all (3 of 130 here: session-limit kills), a session that called tools
    # and wrote no file (41 of 130: it worked through the shell, or it only
    # read), and a session that wrote. Merged, the first two read as "built
    # nothing", which is a finding rather than the absence of one.
    if not r["toolCalls"]:
        r["wroteValue"] = WROTE_NO_TOOLS
    else:
        r["wroteValue"] = encode_touched(r["wrote"])
    # THE DENOMINATOR, AT THE SAME INSTANT AS THE NUMERATOR: file-path tool
    # calls out of ALL tool calls. `no-file-write 0/57` is a session that did
    # 57 things through the shell; `no-file-write 0/0` is a session that did
    # nothing. Same cell, different facts, and the pair is what separates them.
    r["fileToolsValue"] = "%d/%d" % (r["fileTools"], r["toolCalls"])
    return r


# ------------------------------------------------------------------ the log

def log_path(root=None):
    return pathlib.Path(root or REPO) / TURNS_LOG


def append_row(row, root=None):
    """One row, appended. The header is written only when the file is absent,
    so this file is append-only by construction (rule 5)."""
    p = log_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or not p.stat().st_size:
        p.write_text("\t".join(COLUMNS) + "\n", encoding="utf-8")
    # A TAB IN A VALUE WOULD SPLIT THE ROW, the same fault as a space in a
    # verdict value: every reader of this file splits on tabs.
    clean = [str(v).replace("\t", " ").replace("\n", " ").replace("\r", " ")
             for v in row]
    with p.open("a", encoding="utf-8") as fh:
        fh.write("\t".join(clean) + "\n")
    return p


def header_drift(path):
    """(namedInHeader, writtenPerRow, theCorrection) when the live log's
    header names fewer columns than rows now carry, else None.

    WHY THIS PRINTS RATHER THAN FIXES. `append_row` writes the header only
    when the file is absent, which is what makes this file append-only by
    construction (rule 5), and the live `.claude/agent-turns.tsv` was created
    with six columns on 2026-09-03. Every reader here takes columns BY
    POSITION with a length guard, so the stale header costs no reading; it
    costs a HUMAN running `head -1`. The same drift was hand-corrected once
    on `.claude/agent-log.tsv` (2026-09-10, a metadata correction and not a
    measurement). A builder does not edit a live log, so this names the
    one-line correction instead of taking it."""
    try:
        first = pathlib.Path(path).read_text(
            encoding="utf-8", errors="replace").splitlines()[0]
    except (OSError, IndexError):
        return None
    got = first.split("\t")
    if got[0].strip() != "when" or len(got) >= len(COLUMNS):
        return None
    return (len(got), len(COLUMNS), "\\t".join(COLUMNS))


def read_log(path):
    """(rows, short, unmeasured). THREE BUCKETS, not two, because they are
    three different facts and a reader that merged them would print a clean
    denominator over a set it never examined:

      rows        a spawn with a tier and a turn count
      short       a row this reader cannot parse, including the 2-column rows
                  in `.claude/agent-log.tsv` written before this tool existed.
                  Padding one would invent a turn count. A row carrying the
                  SIX pre-2026-09-21 columns is NOT short: it parses, and its
                  `wrote` reads `pre-column` (queue 370).
      unmeasured  a spawn that WAS recorded and whose transcript was already
                  gone at SubagentStop. It happened; its turns are unknown;
                  it must not sit in a median as a zero.
    """
    rows, short, unmeasured = [], 0, 0
    p = pathlib.Path(path)
    if not p.exists():
        return None, 0, 0
    for i, line in enumerate(p.read_text(encoding="utf-8",
                                         errors="replace").splitlines()):
        if not line.strip():
            continue
        cols = line.split("\t")
        if i == 0 and cols[0].strip() == "when":
            continue
        if len(cols) < len(LEGACY_COLUMNS):
            short += 1
            continue
        d = dict(zip(COLUMNS, cols))
        if len(cols) < len(COLUMNS):
            # A ROW THAT PREDATES THE COLUMN IS NOT A MALFORMED ROW, and it is
            # not a row that wrote nothing. It is a row this reader can answer
            # tier and turns for and CANNOT answer "what did it touch" for,
            # ever: nothing rewrites it, the transcript behind it is gone with
            # its container. Marked so, counted by every reader below, and
            # never padded into an invented answer (rule 3b).
            d["wrote"] = PRE_COLUMN
            d["fileToolsOfAll"] = PRE_COLUMN
        if d["tier"] == NOTHING_MEASURED or d["turns"] == NOTHING_MEASURED:
            unmeasured += 1
            continue
        try:
            d["turns"] = int(d["turns"])
            d["alines"] = int(d["alines"])
        except ValueError:
            short += 1
            continue
        if d["turns"] < 0:
            unmeasured += 1
            continue
        rows.append(d)
    return rows, short, unmeasured


# --------------------------------------------------------------- the reading

def by_tier(rows):
    """{tier: [rows]} for every tier in KNOWN_TIERS plus any tier the rows
    actually carry. A KNOWN tier with no rows is present and EMPTY, so the
    report can print the words rather than a zero."""
    out = {t: [] for t in KNOWN_TIERS}
    for r in rows:
        out.setdefault(r["tier"].split("+")[0], []).append(r)
    return out


def tier_line(tier, rows):
    """One tier's reading, and every statistic says what it is a statistic OF.

    NO SPACES IN ANY VALUE: this line is a key=value channel and every reader
    of one splits on whitespace.
    """
    if not rows:
        return ("%-8s spawns=0/%s turnsMedian=%s turnsPeak=%s turnsTotal=%s"
                % (tier, NOTHING_MEASURED, NOTHING_MEASURED, NOTHING_MEASURED,
                   NOTHING_MEASURED))
    turns = sorted(r["turns"] for r in rows)
    peak = max(rows, key=lambda r: r["turns"])
    # THE PEAK CARRIES THE SPAWN IT CAME FROM, at the instant it peaked: a
    # peak with no owner cannot be looked up, and the next reader re-derives
    # it from a different window and gets a different number.
    return ("%-8s spawns=%d turnsMedian=%d turnsPeak=%d@%s turnsTotal=%d "
            "alinesTotal=%d turnsMin=%d"
            % (tier, len(rows), int(statistics.median(turns)), peak["turns"],
               (peak.get("agentId") or peak.get("agent") or "unknown")[:18],
               sum(turns), sum(r["alines"] for r in rows), turns[0]))


def report(rows, short, source, spawn_rows=None, unmeasured=0):
    """Every zero here ships the denominator that produced it."""
    print("spawn-cost: source=%s" % source)
    if rows is None:
        print("  %s: no turns log at %s. The SubagentStop hook that writes it "
              "is not registered in .claude/settings.json, so no spawn has "
              "recorded a tier or a turn count yet." % (NOTHING_MEASURED,
                                                        TURNS_LOG))
        return 2
    if not rows:
        print("  %s: the log exists and carries 0 usable row(s) (%d short or "
              "unparseable, %d recorded but unmeasurable)"
              % (NOTHING_MEASURED, short, unmeasured))
        return 2
    groups = by_tier(rows)
    print("  %d spawn(s) with a tier and a turn count, %d recorded but "
          "unmeasurable (transcript already gone), %d short or unparseable"
          % (len(rows), unmeasured, short))
    if spawn_rows is not None:
        # THE PAIRED READING: how many of the spawns the START log counted
        # produced a stop row at all. Two files, one denominator, and the gap
        # is interrupted spawns plus everything spawned before the hook.
        print("  coverage: %d of %d spawn(s) in %s carry a turn record"
              % (len(rows), spawn_rows, ".claude/agent-log.tsv"))
    for tier in sorted(groups, key=lambda t: (t not in KNOWN_TIERS, t)):
        print("  " + tier_line(tier, groups[tier]))
    allturns = sorted(r["turns"] for r in rows)
    print("  ALL TIERS TOGETHER, which is the statistic every estimate in this "
          "project has been using: spawns=%d turnsMean=%.1f turnsMedian=%d "
          "turnsPeak=%d" % (len(allturns), sum(allturns) / len(allturns),
                            int(statistics.median(allturns)), max(allturns)))
    print("  the mean above is the number that hides the tiers; the per-tier "
          "medians are what a per-tier estimate reads")
    return 0


# --------------------------------------------------------- the printer first

def series(directory, limit=0):
    """THE PRINTER THAT COMES BEFORE ANY BOUND. Every transcript under
    `directory`, one line each, then the same per-tier reading.

    This is how the first real series was read on 2026-09-03: the hook was not
    registered yet, and a bound guessed before the series is a rounding in a
    measurement's clothes."""
    d = pathlib.Path(directory)
    every = sorted(d.rglob("*.jsonl")) if d.is_dir() else []
    # ONLY THE SPAWNS. The parent session transcript sits beside them and is
    # not a spawn: it read 5,754 turns into the first run of this printer and
    # took the opus peak with it. Excluded BY NAME with its count, because an
    # exclusion nobody prints is the same as a cap nobody announces.
    files = [f for f in every if f.parent.name == "subagents"]
    excluded = [f for f in every if f.parent.name != "subagents"]
    if not files:
        print("spawn-cost --transcripts: %s, no .jsonl under %s"
              % (NOTHING_MEASURED, directory))
        return 2
    shown = files if not limit else files[:limit]
    rows = []
    for f in files:
        t = read_transcript(f)
        rows.append({"when": datetime.datetime.utcfromtimestamp(
                        f.stat().st_mtime).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "agent": "unknown", "tier": t["tier"],
                     "turns": t["turns"], "alines": t["alines"],
                     "agentId": f.stem, "why": t["synth_text"],
                     "wrote": t["wroteValue"],
                     "fileToolsOfAll": t["fileToolsValue"]})
    print("spawn-cost --transcripts: %s" % directory)
    if excluded:
        print("  %d transcript(s) EXCLUDED as not-a-spawn (outside a "
              "subagents/ directory): %s"
              % (len(excluded), cap([f.stem for f in excluded], keep=2,
                                    width=30, sep=", ")))
    # TWO NUMBERS, NOT ONE, because they are two different facts and the
    # first version of this line printed the larger one under the smaller
    # one's sentence: a spawn can hit the limit AFTER doing work, and 21 of
    # these did. `noticed` is who saw the wall; `dead` is who never moved.
    noticed = [r for r in rows if "limit" in r.get("why", "")]
    dead = [r for r in noticed if r["turns"] == 0]
    if noticed:
        print("  %d of %d spawn(s) carry a session-limit notice, and %d of "
              "those %d produced NO turn at all: a spawn slot spent on "
              "nothing. Example notice: %s"
              % (len(noticed), len(files), len(dead), len(noticed),
                 cap(sorted({r["why"] for r in noticed}), keep=1, width=60)))
    print("  %d transcript(s) walked%s"
          % (len(files),
             "" if not limit else ", %d shown (+%d more not shown of %d)"
             % (len(shown), len(files) - len(shown), len(files))))
    for r in sorted(rows, key=lambda r: -r["turns"])[:len(shown)]:
        print("    %-24s tier=%-12s turns=%-4d alines=%d"
              % (r["agentId"][:24], r["tier"], r["turns"], r["alines"]))
    if limit and len(files) > len(shown):
        print("    (+%d more not shown of %d)" % (len(files) - len(shown),
                                                  len(files)))
    print("")
    # THE TRANSCRIPTS CARRY NO AGENT TYPE. `agent_type` is a hook field and
    # nothing else writes it, so this series is per TIER only. Said out loud
    # rather than left for a reader to notice the column is always `unknown`.
    print("  the agent TYPE is not in a transcript: it is a SubagentStop hook "
          "field, so this series is per tier and per turn only")
    return report(rows, 0, "transcripts:" + str(directory))


# ------------------------------------------------------------------ the hook

def hook(stdin_text, root=None, now=None):
    """SubagentStop. Returns (row, why) with row None when nothing was
    written. NEVER RAISES: the caller exits 0 whatever happens here."""
    try:
        d = json.loads(stdin_text)
    except ValueError:
        return None, "stdin is not JSON"
    if not isinstance(d, dict):
        return None, "stdin is not an object"
    agent = (d.get("agent_type") or "").strip()
    if not agent:
        # NOTHING PARSED, NOTHING WRITTEN: a row with an empty agent column
        # reads as "an agent with no name ran", which is a finding; the truth
        # is that the hook could not tell, and those must not look alike.
        return None, "no agent_type in the payload"
    tpath = d.get("agent_transcript_path") or ""
    if tpath and pathlib.Path(tpath).exists():
        t = read_transcript(tpath, root)
    else:
        # THE FIELD IS OPTIONAL AND THE FILE MAY BE GONE. Record the spawn
        # with the words, never with a 0 that reads as a spawn that did
        # nothing.
        t = {"turns": NOTHING_MEASURED, "alines": NOTHING_MEASURED,
             "tier": NOTHING_MEASURED, "wroteValue": NOTHING_MEASURED,
             "fileToolsValue": NOTHING_MEASURED}
    when = (now or datetime.datetime.now(datetime.timezone.utc)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    row = (when, agent, t["tier"], t["turns"], t["alines"],
           d.get("agent_id") or "unknown", t["wroteValue"],
           t["fileToolsValue"])
    append_row(row, root)
    return row, "appended"


# ------------------------------------------------------------------ selftest

# ACCEPTING FIRST. The expensive failure is a reader that cannot see a normal
# spawn, which would send every future estimate back to the flat average this
# tool exists to replace.
def _jsonl(entries):
    return "\n".join(json.dumps(e) for e in entries) + "\n"


GOOD_TRANSCRIPT = _jsonl([
    {"type": "user", "message": {"role": "user", "content": "go"}},
    {"type": "assistant", "message": {"id": "m1", "model": "claude-opus-5"}},
    {"type": "assistant", "message": {"id": "m1", "model": "claude-opus-5"}},
    {"type": "assistant", "message": {"id": "m2", "model": "claude-opus-5"}},
])
FABLE_TRANSCRIPT = _jsonl([
    {"type": "assistant", "message": {"id": "f1", "model": "claude-fable-5"}},
])
SYNTH_ONLY = _jsonl([
    {"type": "assistant", "message": {"id": "s1", "model": "<synthetic>"}},
])
MIXED = _jsonl([
    {"type": "assistant", "message": {"id": "x1", "model": "claude-opus-5"}},
    {"type": "assistant", "message": {"id": "x2", "model": "claude-opus-5"}},
    {"type": "assistant", "message": {"id": "x3", "model": "claude-fable-5"}},
])


def _tmp(text, name="t.jsonl"):
    import atexit
    import shutil
    import tempfile
    d = pathlib.Path(tempfile.mkdtemp(prefix="spawn-cost-"))
    atexit.register(shutil.rmtree, str(d), True)
    p = d / name
    p.write_text(text, encoding="utf-8")
    return p


def selftest():
    import atexit
    import shutil
    passed, failed = 0, []

    def ok(name, cond, got=""):
        nonlocal passed
        if cond:
            passed += 1
            print("  ok   %s" % name)
        else:
            failed.append(name)
            print("  FAIL %s\n         got: %r" % (name, got))

    print("spawn-cost --selftest: ACCEPTING CASES FIRST\n")
    t = read_transcript(_tmp(GOOD_TRANSCRIPT))
    ok("a normal opus transcript reads as opus", t["tier"] == "opus", t["tier"])
    ok("two distinct message ids over three assistant lines is 2 turns, "
       "3 alines", (t["turns"], t["alines"]) == (2, 3), (t["turns"], t["alines"]))
    tf = read_transcript(_tmp(FABLE_TRANSCRIPT))
    ok("a fable transcript reads as fable", tf["tier"] == "fable", tf["tier"])
    tm = read_transcript(_tmp(MIXED))
    ok("a transcript that changed model mid-run is marked mixed, not averaged "
       "into one tier", tm["tier"] == "opus+mixed", tm["tier"])

    print("\n  THE CASES A ZERO WOULD LIE ABOUT:\n")
    ts = read_transcript(_tmp(SYNTH_ONLY))
    ok("a transcript of nothing but synthetic lines is %s, never a one-turn "
       "spawn" % NO_TIER, ts["tier"] == NO_TIER and ts["turns"] == 0,
       (ts["tier"], ts["turns"]))
    tb = read_transcript(_tmp("{not json\n" + GOOD_TRANSCRIPT))
    ok("a malformed line is COUNTED as unparsed, not dropped in silence",
       tb["unparsed"] == 1 and tb["turns"] == 2, (tb["unparsed"], tb["turns"]))
    tn = read_transcript("/nonexistent/agent.jsonl")
    ok("a transcript that is not there reads as the words",
       tn["tier"] == NOTHING_MEASURED, tn["tier"])
    ok("a tier with no rows prints the words, never 0",
       NOTHING_MEASURED in tier_line("sonnet", []), tier_line("sonnet", []))
    ok("and the words carry no space, because this is a key=value line",
       " " not in tier_line("sonnet", []).split("spawns=")[1].split()[0],
       tier_line("sonnet", []))

    print("\n  THE HOOK, both ways:\n")
    import tempfile
    root = pathlib.Path(tempfile.mkdtemp(prefix="spawn-cost-root-"))
    import atexit
    import shutil
    atexit.register(shutil.rmtree, str(root), True)
    tp = _tmp(GOOD_TRANSCRIPT, "agent-abc.jsonl")
    row, why = hook(json.dumps({"hook_event_name": "SubagentStop",
                                "agent_type": "systems-builder",
                                "agent_id": "agent-abc",
                                "agent_transcript_path": str(tp)}), root)
    ok("a real SubagentStop payload appends one row carrying tier and turns",
       row is not None and row[1] == "systems-builder" and row[2] == "opus"
       and row[3] == 2, (row, why))
    rows, short, unmeas = read_log(log_path(root))
    ok("and the row reads back with its tier and its turn count",
       len(rows) == 1 and rows[0]["tier"] == "opus" and rows[0]["turns"] == 2,
       rows)
    ok("the header names every column it writes",
       log_path(root).read_text().splitlines()[0].split("\t") == list(COLUMNS),
       log_path(root).read_text().splitlines()[0])
    row2, why2 = hook("{ not json", root)
    ok("malformed stdin writes nothing and says why", row2 is None, (row2, why2))
    row3, why3 = hook(json.dumps({"hook_event_name": "SubagentStop"}), root)
    ok("a payload with no agent_type writes nothing rather than a nameless row",
       row3 is None, (row3, why3))
    row4, _ = hook(json.dumps({"agent_type": "planner",
                               "agent_transcript_path": "/gone.jsonl"}), root)
    ok("a missing transcript records the words, never turns=0",
       row4 is not None and row4[2] == NOTHING_MEASURED, row4)
    rows, short, unmeas = read_log(log_path(root))
    ok("the unmeasurable row is COUNTED in its own bucket, never as a "
       "0-turn spawn in a median",
       len(rows) == 1 and unmeas == 1 and short == 0,
       (len(rows), unmeas, short))

    print("\n  THE OLD LOG SHAPE, which must not be padded into invented data:\n")
    old = root / "old.tsv"
    old.write_text("when\tagent\n2026-09-03T10:00:00Z\tplanner\n",
                   encoding="utf-8")
    rows, short, unmeas = read_log(old)
    ok("a 2-column row from .claude/agent-log.tsv is counted short, not "
       "given a turn count", rows == [] and short == 1, (rows, short))

    print("\n  ROUTING DRIFT (--routing-drift), both named traps PLANTED:\n")
    droot = pathlib.Path(tempfile.mkdtemp(prefix="spawn-cost-drift-"))
    (droot / ".claude" / "agents").mkdir(parents=True)
    (droot / ".claude" / "agents" / "worker.md").write_text(
        "---\nname: worker\nmodel: opus\n---\nbody\n", encoding="utf-8")
    turns_log = droot / TURNS_LOG
    turns_log.parent.mkdir(parents=True, exist_ok=True)
    turns_log.write_text(
        "\t".join(COLUMNS) + "\n"
        # TRAP 1: one agentId, SIX snapshot rows, climbing turns. Summed,
        # this alone would read 45+68+83+105+122+162=585 turns for one
        # spawn; last-wins must read 162.
        + "2026-09-01T00:00:00Z\tworker\topus\t45\t80\tclimb1\n"
        + "2026-09-01T00:01:00Z\tworker\topus\t68\t120\tclimb1\n"
        + "2026-09-01T00:02:00Z\tworker\topus\t83\t150\tclimb1\n"
        + "2026-09-01T00:03:00Z\tworker\topus\t105\t190\tclimb1\n"
        + "2026-09-01T00:04:00Z\tworker\topus\t122\t220\tclimb1\n"
        + "2026-09-01T00:05:00Z\tworker\topus\t162\t290\tclimb1\n"
        # A genuine disagreement: declared opus, ran fable.
        + "2026-09-02T00:00:00Z\tworker\tfable\t9\t15\tdisagree1\n"
        # TRAP 2: a built-in type with no definition file on disk.
        + "2026-09-02T01:00:00Z\tgeneral-purpose\topus\t30\t50\tnodecl1\n",
        encoding="utf-8")
    d = routing_drift(droot)
    ok("distinct agentId count is 3, one per agentId, not one per row",
       d["distinct"] == 3, d["distinct"])
    ok("TRAP 1: last-wins reads 162 turns for the climbing spawn, never "
       "the 585-turn sum of all six snapshots",
       d["agreements"] == 1, d["agreements"])   # climb1 agrees: opus==opus
    ok("TRAP 2: general-purpose (no definition) is excluded from the "
       "numerator, not counted as a disagreement",
       d["noDeclaration"] == 1 and d["noDeclarationNames"] == ["general-purpose"],
       (d["noDeclaration"], d["noDeclarationNames"]))
    ok("the one real disagreement (declared opus, ran fable) is bucketed "
       "with its 9 turns, not the climbing spawn's 162 or 585",
       d["buckets"] == [{"declared": "opus", "ran": "fable", "agents": 1,
                        "turns": 9, "whenMin": "2026-09-02T00:00:00Z",
                        "whenMax": "2026-09-02T00:00:00Z"}],
       d["buckets"])
    ok("totalTurns is 162+9+30=201, never 585+9+30 from summing the "
       "climbing snapshots", d["totalTurns"] == 201, d["totalTurns"])
    d_missing = routing_drift(pathlib.Path(tempfile.mkdtemp(prefix="spawn-cost-nolog-")))
    ok("NEVER-RAN: no turns log at all reads rows=None, not an empty drift",
       d_missing.get("rows") is None, d_missing)
    ok("with no git repository at all, committed model reads as unknown and "
       "nothing is excluded as pre-ruling (0 of 3 agentIds)",
       d["preRuling"] == 0, d["preRuling"])
    shutil.rmtree(droot, ignore_errors=True)

    print("\n  PRE-RULING (the director's correction, 2026-09-10): a row "
          "CANNOT violate a declaration that postdates it, PLANTED:\n")
    proot = pathlib.Path(tempfile.mkdtemp(prefix="spawn-cost-preruling-"))

    def run_git(*args):
        subprocess.run(["git", "-C", str(proot)] + list(args),
                       capture_output=True, text=True, check=True)
    (proot / ".claude" / "agents").mkdir(parents=True)
    worker_md = proot / ".claude" / "agents" / "worker.md"
    worker_md.write_text("---\nname: worker\nmodel: opus\n---\nbody\n",
                         encoding="utf-8")
    run_git("init", "-q")
    run_git("config", "user.email", "t@t")
    run_git("config", "user.name", "t")
    run_git("add", "-A")
    run_git("commit", "-q", "-m", "worker: opus, the committed declaration")
    # THE RECLASSIFICATION, uncommitted, exactly as the live ruling left the
    # real nine definitions: working tree says sonnet, HEAD still says opus.
    worker_md.write_text("---\nname: worker\nmodel: sonnet\n---\nbody\n",
                         encoding="utf-8")
    ptlog = proot / TURNS_LOG
    ptlog.parent.mkdir(parents=True, exist_ok=True)
    ptlog.write_text(
        "\t".join(COLUMNS) + "\n"
        # PLANTED: ran opus, long before the reclassification -- compliance
        # with the rule as it THEN stood (declared opus, ran opus), not a
        # disagreement with the rule as it stands now (declared sonnet).
        + "2020-01-01T00:00:00Z\tworker\topus\t50\t90\told1\n",
        encoding="utf-8")
    dp = routing_drift(proot)
    ok("a row predating its agent's reclassification lands in preRuling "
       "(1 row, 50 turns), not the violation count",
       dp["preRuling"] == 1 and dp["preRulingTurns"] == 50, dp)
    ok("and it is NOT counted as an agreement either (it was never judged "
       "against the new declaration at all)", dp["agreements"] == 0,
       dp["agreements"])
    ok("and the violation buckets are empty: the ONLY row on file is the "
       "pre-ruling one", dp["buckets"] == [] and dp["disagreeAgents"] == 0,
       (dp["buckets"], dp["disagreeAgents"]))
    shutil.rmtree(proot, ignore_errors=True)


    print("\n  E370, WHAT A SESSION TOUCHED. ACCEPTING FIRST, AND THE LIVE "
          "REPOSITORY IS THE ACCEPTING FIXTURE:\n")
    # A transcript shaped exactly like the live ones: one assistant message
    # carrying tool_use blocks. Two edits into the game layer, one write into
    # the studio layer, one Read and one Bash that are NOT writes.
    TOUCHED = _jsonl([
        {"type": "assistant", "message": {"id": "t1", "model": "claude-opus-5",
         "content": [
            {"type": "tool_use", "name": "Edit", "input": {
                "file_path": str(REPO / "ledger/Assets/Scripts/Sim.cs")}},
            {"type": "tool_use", "name": "Edit", "input": {
                "file_path": str(REPO / "ledger/Assets/Scripts/Npc.cs")}},
            {"type": "tool_use", "name": "Write", "input": {
                "file_path": str(REPO / "tools/made-up.py")}},
            {"type": "tool_use", "name": "Read", "input": {
                "file_path": str(REPO / "canon.md")}},
            {"type": "tool_use", "name": "Bash", "input": {
                "command": "python3 ledger/verify.py"}}]}},
    ])
    tt = read_transcript(_tmp(TOUCHED))
    ok("a normal transcript yields the AREAS IT WROTE IN, ordered by write "
       "calls, from the same read that gave tier and turns",
       tt["wroteValue"] == "ledger/Assets:2,tools:1", tt["wroteValue"])
    ok("and the denominator rides beside it AT THE SAME INSTANT: 3 file-tool "
       "calls of 5 tool calls, so `no-file-write 0/57` can never be confused "
       "with `no-file-write 0/0`",
       tt["fileToolsValue"] == "3/5", tt["fileToolsValue"])
    ok("a Read is NOT a write: canon.md was opened and is in no area",
       "." not in tt["wrote"] and tt["fileTools"] == 3, tt["wrote"])
    ok("a Bash call is counted in the denominator and names no area: its "
       "paths are NOT recoverable and are not guessed at",
       tt["bashCalls"] == 1, tt["bashCalls"])
    # THE LIVE CODEBASE AS THE ACCEPTING FIXTURE. These four paths exist in
    # this repository right now; the assertion is pinned to them so that a
    # reorganisation shows up here rather than silently reclassifying work.
    live = {"tools/spawn-cost.py": ("tools", SIDE_STUDIO),
            "ledger/verify.py": ("ledger", SIDE_STUDIO),
            ".claude/hooks/log-agent.sh": (".claude/hooks", SIDE_STUDIO),
            "canon.md": (".", SIDE_UNKNOWN)}
    missing = [f for f in live if not (REPO / f).exists()]
    ok("the four live files this fixture is pinned to all exist (%d checked)"
       % len(live), not missing, missing)
    bad = [(f, rel_area(str(REPO / f)), area_side(rel_area(str(REPO / f))))
           for f, want in live.items()
           if (rel_area(str(REPO / f)), area_side(rel_area(str(REPO / f))))
           != want]
    ok("and each reads as the area and the side the table claims (the "
       "filename is dropped, the directory is capped at %d)" % AREA_DEPTH,
       not bad, bad)
    ok("a game path under ledger/ is game, and the studio's own checkers "
       "living under ledger/ are studio: the one boundary this repo draws "
       "by hand",
       area_side(rel_area(str(REPO / "ledger/Assets/Scripts/A.cs")))
       == SIDE_GAME
       and area_side(rel_area(str(REPO / "ledger/Soak/B.cs"))) == SIDE_STUDIO,
       (rel_area(str(REPO / "ledger/Assets/Scripts/A.cs")),
        rel_area(str(REPO / "ledger/Soak/B.cs"))))
    # THE LIVE TURNS LOG AS THE ACCEPTING FIXTURE, and this one guards the
    # exact regression adding two columns could have caused: every row on
    # disk was written with six, and a length guard against the NEW width
    # would have turned all of them into "short" and collapsed every reading
    # this tool already gives.
    live_rows, live_short, live_unmeas = read_log(log_path())
    ok("the LIVE turns log still parses after the column was added: %s row(s) "
       "usable, %s short"
       % (len(live_rows) if live_rows else 0, live_short),
       live_rows and len(live_rows) > 100 and live_short == 0,
       (len(live_rows or []), live_short, live_unmeas))
    # A FIXTURE PINNED TO A LIVE ASSET MUST NOT BREAK WHEN THE WORK IS DONE.
    # The first draft of this assertion said EVERY live row reads pre-column,
    # and it went red within the hour: the SubagentStop hook started writing
    # eight-column rows, which is the instrument WORKING. The invariant that
    # actually holds for ever is the other way round: the 325 rows that
    # existed when the column landed on 2026-09-21 can never acquire one and
    # can never be rewritten, so the pre-column count is a FLOOR that only
    # holds still.
    live_pre = [r for r in (live_rows or []) if r["wrote"] == PRE_COLUMN]
    ok("the 325 live rows that predate the column still read `pre-column` "
       "and never `no-file-write`: %d found, and that count can only hold "
       "still because nothing rewrites a row" % len(live_pre),
       len(live_pre) >= 325, len(live_pre))
    ok("and no live row carries an EMPTY wrote cell, which would read as an "
       "area nobody named",
       live_rows and all((r["wrote"] or "").strip() for r in live_rows),
       [r["agentId"] for r in (live_rows or [])
        if not (r["wrote"] or "").strip()][:3])
    ga_live, ga_src = _game_agents()
    ok("GAME_AGENTS is read from ledger/verify.py and not copied here: one "
       "definition of the withdrawn proxy",
       ga_live and "systems-builder" in ga_live, (ga_src, sorted(ga_live or [])))
    # THE LIVE SPAWN LOG IS THE ACCEPTING FIXTURE for the coverage half.
    # SHAPE, NEVER TODAY'S COUNTS: every number below moves on the next
    # spawn, so what is asserted is that they NEST. Pinning 747 here would
    # make the next agent that runs turn this selftest red for working.
    cen_live = spawn_census()
    ok("the LIVE spawn log is walked once and nests: rows=%s "
       "rowsCarryingAnId=%s distinctIds=%s, ids <= rowsWithId <= rows"
       % (cen_live and cen_live["rows"], cen_live and cen_live["rowsWithId"],
          cen_live and len(cen_live["roles"])),
       cen_live and cen_live["rows"] > 0
       and len(cen_live["roles"]) <= cen_live["rowsWithId"]
       and cen_live["rowsWithId"] <= cen_live["rows"],
       cen_live)
    ok("and `_roles` is that same walk and not a second one, so the join and "
       "the denominator can never disagree",
       _roles() == (cen_live or {}).get("roles"),
       (len(_roles()), len((cen_live or {}).get("roles") or {})))
    wl_live = work_split(live_rows or [], (cen_live or {}).get("roles") or {},
                         ga_live, cen_live)
    ok("the LIVE coverage pair is consistent in BOTH directions: "
       "noStopRow=%s of %s spawn id(s), noSpawnRow=%s of %s session(s)"
       % (wl_live["noStopRow"], wl_live["spawnIds"], wl_live["noSpawnRow"],
          wl_live["walked"]),
       0 <= wl_live["noStopRow"] <= wl_live["spawnIds"]
       and 0 <= wl_live["noSpawnRow"] <= wl_live["walked"],
       (wl_live["noStopRow"], wl_live["spawnIds"], wl_live["noSpawnRow"],
        wl_live["walked"]))
    ok("and the LIVE structural boundary is read off the file rather than "
       "pinned: firstIdAt=%s, and its two halves add back to the total"
       % wl_live["firstIdAt"],
       wl_live["firstIdAt"]
       and wl_live["noSpawnRowPreId"] + wl_live["noSpawnRowSince"]
       == wl_live["noSpawnRow"],
       (wl_live["firstIdAt"], wl_live["noSpawnRowPreId"],
        wl_live["noSpawnRowSince"], wl_live["noSpawnRow"]))
    ok("and the four stop-log buckets still add to the sessions walked, so "
       "the fifth (noStopRow) was added BESIDE that arithmetic and not "
       "inside it",
       wl_live["answerable"] + wl_live["preColumn"]
       + wl_live["transcriptGone"] + wl_live["noToolCall"]
       + wl_live["noFileWrite"] == wl_live["walked"],
       (wl_live["answerable"], wl_live["preColumn"], wl_live["walked"]))

    print("\n  E370, THE CASES A PARTIAL COLUMN WOULD READ AS A COMPLETE "
          "ONE (rejecting fixtures, synthetic):\n")
    NOWRITE = _jsonl([
        {"type": "assistant", "message": {"id": "n1", "model": "claude-opus-5",
         "content": [
            {"type": "tool_use", "name": "Bash", "input": {
                "command": "cat > tools/x.py <<'EOF'\nprint(1)\nEOF"}},
            {"type": "tool_use", "name": "Read", "input": {
                "file_path": str(REPO / "CLAUDE.md")}}]}},
    ])
    tn2 = read_transcript(_tmp(NOWRITE))
    ok("A PATH WRITTEN THROUGH A SHELL HEREDOC IS NOT RECOVERED AND NOT "
       "GUESSED: the session reads no-file-write with the pair 0/2 saying "
       "two tools DID run",
       (tn2["wroteValue"], tn2["fileToolsValue"]) == (WROTE_NONE, "0/2"),
       (tn2["wroteValue"], tn2["fileToolsValue"]))
    NOTOOLS = _jsonl([
        {"type": "assistant", "message": {"id": "z1", "model": "claude-opus-5",
         "content": [{"type": "text", "text": "I have nothing to do"}]}},
    ])
    tz = read_transcript(_tmp(NOTOOLS))
    ok("a spawn that called NO tool is no-tool-call with the pair 0/0, never "
       "no-file-write: a slot spent on nothing is not a session that chose "
       "to write nothing",
       (tz["wroteValue"], tz["fileToolsValue"]) == (WROTE_NO_TOOLS, "0/0"),
       (tz["wroteValue"], tz["fileToolsValue"]))
    tgone = read_transcript("/nonexistent/agent370.jsonl")
    ok("a transcript that is GONE reads the words in BOTH cells, never "
       "no-file-write",
       (tgone["wroteValue"], tgone["fileToolsValue"])
       == (NOTHING_MEASURED, NOTHING_MEASURED),
       (tgone["wroteValue"], tgone["fileToolsValue"]))
    OUTSIDE = _jsonl([
        {"type": "assistant", "message": {"id": "o1", "model": "claude-opus-5",
         "content": [
            {"type": "tool_use", "name": "Write", "input": {
                "file_path": "/tmp/scratch/notes.md"}}]}},
    ])
    tout = read_transcript(_tmp(OUTSIDE))
    ok("A PATH OUTSIDE THE REPOSITORY is COUNTED and lands in no area: the "
       "scratchpad is not work, and inventing an area for it would put "
       "/tmp on one side of the split",
       (tout["outsideRepo"], tout["wroteValue"], tout["fileToolsValue"])
       == (1, WROTE_NONE, "1/1"),
       (tout["outsideRepo"], tout["wroteValue"], tout["fileToolsValue"]))
    ok("A SYNTHETIC AREA THAT EXISTS NOWHERE is unclassified, never quietly "
       "studio: zzz-no-such-area-370 is in no table and must say so",
       area_side("zzz-no-such-area-370/deep") == SIDE_UNKNOWN,
       area_side("zzz-no-such-area-370/deep"))
    many = {("a%02d" % i): (20 - i) for i in range(12)}
    v = encode_touched(many)
    back, ha, hc = decode_touched(v)
    ok("THE CAP ANNOUNCES WHEN IT BITES: 12 areas encode to %d shown plus "
       "+4more carrying the rest, and it decodes back to the same hidden "
       "counts" % AREAS_KEPT,
       ",+4more:" in v and len(back) == AREAS_KEPT and ha == 4
       and hc == sum(sorted(many.values())[:4]), (v, ha, hc))
    ok("and the cell carries no space and no tab, because every reader of "
       "this file splits on one or the other",
       " " not in v and "\t" not in v, v)
    ok("an empty area map encodes to the words, never to a blank cell",
       encode_touched({}) == WROTE_NONE, encode_touched({}))
    ok("and each sentinel decodes to an EMPTY map so no caller can read one "
       "as an area (they are bucketed by name, not by shape)",
       all(decode_touched(x) == ({}, 0, 0)
           for x in (WROTE_NONE, WROTE_NO_TOOLS, PRE_COLUMN,
                     NOTHING_MEASURED, "")),
       [decode_touched(x) for x in (WROTE_NONE, PRE_COLUMN)])

    print("\n  E370, THE PARTIAL COLUMN ITSELF, PLANTED (rule 5b: a run "
          "where the thing it asserts CAN happen):\n")
    import tempfile as _tf
    sroot = pathlib.Path(_tf.mkdtemp(prefix="spawn-cost-370-"))
    atexit.register(shutil.rmtree, str(sroot), True)
    slog = sroot / TURNS_LOG
    slog.parent.mkdir(parents=True, exist_ok=True)
    slog.write_text(
        "\t".join(LEGACY_COLUMNS) + "\n"
        # SIX COLUMNS: a row written before the column existed.
        + "2026-09-01T00:00:00Z\tplanner\topus\t20\t40\told370\n"
        # EIGHT: a row that carries it.
        + "2026-09-21T00:00:00Z\tsystems-builder\topus\t30\t60\tnew370\t"
          "ledger/Assets:4\t4/9\n",
        encoding="utf-8")
    mixed, mshort, _mu = read_log(slog)
    ok("a six-column row and an eight-column row in ONE file both parse, and "
       "0 of 2 are short", len(mixed) == 2 and mshort == 0,
       (len(mixed), mshort))
    w = work_split(mixed, {}, frozenset(("systems-builder",)))
    ok("THE PARTIAL COLUMN CANNOT READ AS A COMPLETE ONE: answerable=1 and "
       "preColumn=1 of 2 walked, and the pre-column row is in NEITHER the "
       "numerator nor the no-file-write bucket",
       (w["walked"], w["answerable"], w["preColumn"], w["noFileWrite"])
       == (2, 1, 1, 0),
       (w["walked"], w["answerable"], w["preColumn"], w["noFileWrite"]))
    # PLANTED, THE FIFTH BUCKET: a spawn that never reached SubagentStop is
    # in NONE of the four above, so it is counted against the spawn log's own
    # census. The two ghosts are synthetic ids that exist in no live file, so
    # doing the work this tool prompts can never break this fixture.
    scensus = sroot / ".claude" / "agent-log.tsv"
    scensus.parent.mkdir(parents=True, exist_ok=True)
    scensus.write_text(
        "when\tagent\tmodel\treason\tagentId\n"
        # A row from before the agentId column: two columns, joinable to
        # nothing, and it must still be COUNTED in rowsCumulative.
        "2026-08-24T16:54:19Z\tgeneral-purpose\n"
        "2026-09-21T00:00:00Z\tsystems-builder\topus\tdefault\tnew370\n"
        "2026-09-21T00:00:01Z\tplanner\topus\tdefault\tzzz-ghost370a\n"
        "2026-09-21T00:00:02Z\tplanner\topus\tdefault\tzzz-ghost370b\n",
        encoding="utf-8")
    cen = spawn_census(sroot)
    ok("PLANTED: the spawn census counts a row that carries NO id rather "
       "than dropping it: rows=4 rowsWithId=3 distinctIds=3",
       (cen["rows"], cen["rowsWithId"], len(cen["roles"])) == (4, 3, 3),
       (cen["rows"], cen["rowsWithId"], len(cen["roles"])))
    wc = work_split(mixed, cen["roles"], frozenset(("systems-builder",)), cen)
    ok("PLANTED, THE FIFTH BUCKET: 2 spawn id(s) of 3 never reached "
       "SubagentStop and are in NO bucket of the four, and 1 session of 2 "
       "here has no spawn row -- both directions counted",
       (wc["noStopRow"], wc["spawnIds"], wc["noSpawnRow"], wc["walked"])
       == (2, 3, 1, 2),
       (wc["noStopRow"], wc["spawnIds"], wc["noSpawnRow"], wc["walked"]))
    import contextlib as _ctx
    import io as _io
    _buf = _io.StringIO()
    with _ctx.redirect_stdout(_buf):
        report_work_split(wc, "fixture", "fixture")
    _out = _buf.getvalue()
    # EXACT WHITESPACE TOKENS, not substrings. The substring form of this
    # assertion passed while the line ended `spawnIdsWithNoStopRow=2/3:` and
    # ledger/verify.py's reader took the colon as part of the number.
    _toks = set(_out.split())
    ok("and the REPORT says so in tokens a grep can take WHOLE, each beside "
       "its own denominator and none carrying punctuation",
       {"spawnRowsCumulative=4", "rowsCarryingAnId=3/4",
        "distinctSpawnIds=3", "spawnIdsWithNoStopRow=2/3",
        "stopIdsWithNoSpawnRow=1/2"} <= _toks,
       [t for t in sorted(_toks) if t.startswith(("spawn", "stop", "rows",
                                                  "distinct"))][:6])
    ok("and no coverage value carries a space, because every reader of a "
       "key=value line splits on whitespace",
       all(" " not in tok.split("=", 1)[1]
           for line in _out.splitlines() for tok in line.split()
           if tok.startswith(("spawnRowsCumulative=", "rowsCarryingAnId=",
                              "distinctSpawnIds=", "spawnIdsWithNoStopRow=",
                              "stopIdsWithNoSpawnRow="))),
       [l for l in _out.splitlines() if "spawnRowsCumulative" in l])
    ok("PLANTED: the 1 session with no spawn row is dated BEFORE the first "
       "id the spawn log ever carried, so it reads structural and not as a "
       "hook failing now",
       (wc["firstIdAt"], wc["noSpawnRowPreId"], wc["noSpawnRowSince"])
       == ("2026-09-21T00:00:00Z", 1, 0),
       (wc["firstIdAt"], wc["noSpawnRowPreId"], wc["noSpawnRowSince"]))
    # PLANTED, THE ALARM: a stop row NEWER than that instant whose id the
    # spawn log never recorded. This is the start hook missing a spawn, and
    # it must not be able to hide inside the structural count.
    missed = list(mixed) + [dict(mixed[1], agentId="zzz-missed370",
                                 when="2026-09-21T02:00:00Z")]
    wm = work_split(missed, cen["roles"], frozenset(("systems-builder",)),
                    cen)
    ok("PLANTED, THE ALARM: a stop row newer than the first recorded id and "
       "absent from the spawn log counts as sinceThatInstant=1, never "
       "folded into the structural half",
       (wm["noSpawnRow"], wm["noSpawnRowPreId"], wm["noSpawnRowSince"])
       == (2, 1, 1),
       (wm["noSpawnRow"], wm["noSpawnRowPreId"], wm["noSpawnRowSince"]))
    # A SPAWN LOG THAT EXISTS AND CARRIES NO ID AT ALL: the boundary cannot
    # be computed, so the line says so instead of printing 0 of 0.
    _buf3 = _io.StringIO()
    _cen0 = {"rows": 1, "rowsWithId": 0, "roles": {}, "firstIdAt": None}
    with _ctx.redirect_stdout(_buf3):
        report_work_split(work_split(mixed, {}, None, _cen0), "fixture",
                          "fixture")
    ok("a spawn log carrying NO id at all cannot say which sessions could "
       "have joined, and prints the words rather than 0",
       "%s: no spawn row carries an id" % NOTHING_MEASURED in _buf3.getvalue(),
       [l for l in _buf3.getvalue().splitlines() if "COULD have joined" in l])
    _buf2 = _io.StringIO()
    with _ctx.redirect_stdout(_buf2):
        report_work_split(work_split(mixed, {}, None, None), "fixture",
                          "fixture")
    ok("NEVER-RAN FOR THE COVERAGE HALF: an unreadable spawn log prints the "
       "words and NOT a zero, because 'saw all of it' and 'could not look' "
       "must never share a number",
       "%s: the spawn log could not be read" % NOTHING_MEASURED
       in _buf2.getvalue()
       and "spawnIdsWithNoStopRow" not in _buf2.getvalue(),
       [l for l in _buf2.getvalue().splitlines() if "SPAWN LOG" in l
        or NOTHING_MEASURED in l][:3])
    ok("and a missing spawn log is None and never an empty census, so no "
       "caller can read it as a log with nothing in it",
       spawn_census(sroot / "no-such-root-370") is None,
       spawn_census(sroot / "no-such-root-370"))
    drift = header_drift(slog)
    ok("and the stale header ANNOUNCES ITSELF rather than being rewritten "
       "under a live log", drift and drift[0] == 6 and drift[1] == 8, drift)
    full = sroot / "full.tsv"
    full.write_text("\t".join(COLUMNS) + "\n", encoding="utf-8")
    ok("a header that already names every column announces nothing: a "
       "notice on a file that is fine trains readers to skip it",
       header_drift(full) is None, header_drift(full))
    # PLANTED: the two facts the role proxy CANNOT express, so the ladder's
    # disagreement count is exercised rather than merely possible.
    planted = [
        {"agentId": "p1", "agent": "systems-builder",
         "wrote": "ledger/Assets:3,tools:2"},          # role game, wrote BOTH
        {"agentId": "p2", "agent": "systems-builder",
         "wrote": "tools:5"},                          # role game, wrote studio
        {"agentId": "p3", "agent": "instrument-builder",
         "wrote": "ledger/Assets:2"},                  # role studio, wrote game
        {"agentId": "p4", "agent": "instrument-builder",
         "wrote": "tools:1"},                          # agrees
        {"agentId": "p5", "agent": "instrument-builder",
         "wrote": "zzz-no-such-area-370:1"},           # unclassified
    ]
    wp = work_split(planted, {}, frozenset(("systems-builder",)))
    ok("PLANTED: a session that wrote in BOTH halves is `both`, which one "
       "role name per row can never say",
       wp["sides"]["both"] == 1, wp["sides"])
    ok("PLANTED: role-says-game/wrote-studio and role-says-studio/wrote-game "
       "are both counted, so the proxy error is a measurement and not an "
       "assumption",
       wp["cross"].get((SIDE_GAME, SIDE_STUDIO)) == 1
       and wp["cross"].get((SIDE_STUDIO, SIDE_GAME)) == 1, wp["cross"])
    ok("PLANTED: a session whose only area is unclassified is answerable and "
       "sits on NEITHER side",
       wp["sides"][SIDE_UNKNOWN] == 1 and wp["answerable"] == 5, wp["sides"])
    ok("the ladder's two halves add up: agree+disagree equals the sessions "
       "carrying both a role and an area",
       sum(wp["cross"].values()) == wp["crossBoth"] == 5,
       (sum(wp["cross"].values()), wp["crossBoth"]))
    ok("with NO GAME_AGENTS table readable, rung 1 is refused for every "
       "session rather than half-answered",
       work_split(planted, {}, None)["roleUnknown"] == 5,
       work_split(planted, {}, None)["roleUnknown"])
    ok("NEVER-RAN: 0 sessions reads as the words and exit 2, never as a "
       "clean split",
       report_work_split(work_split([], {}, ga_live), "fixture", "fixture")
       == 2)
    ok("and a session set whose column answers for NOBODY also exits 2: a "
       "rung printed is not a split computed",
       report_work_split(work_split(
           [{"agentId": "q1", "agent": "planner", "wrote": PRE_COLUMN}],
           {}, ga_live), "fixture", "fixture") == 2)

    print("\nspawn-cost --selftest: %s. %d passed, %d failed"
          % ("PASS" if not failed else "FAILED", passed, len(failed)))
    for f in failed:
        print("  " + f)
    return 0 if not failed else 3


def spawn_census(root=None):
    """ONE walker over `.claude/agent-log.tsv`, three products.

    A second walker over one file is the copy nobody fixes when the first is
    fixed, so `_spawn_rows` and `_roles` both come off this one.

    Returns None when the file is absent (the caller prints the words), else:
      rows        CUMULATIVE rows under the header. This is the SPAWN CENSUS:
                  one row per SubagentStart, resumes included, which is the
                  denominator queue 370's sentence is about.
      rowsWithId  how many of those carry an agentId at all. The column was
                  added after the log started, so the remainder is permanent
                  and can be joined to nothing, ever.
      roles       agentId -> role name, LAST-WINS per id (a resumed spawn
                  writes a second row under the same id).
      firstIdAt   the EARLIEST `when` on a row that carries an id, or None.
                  Not decoration: it is the instant before which no stop row
                  can possibly be joined, so it separates a structural gap
                  from a hook that is failing now. Measured rather than
                  pinned, because the day the column started is a fact of
                  the file and not of this program.
    """
    p = pathlib.Path(root or REPO) / ".claude" / "agent-log.tsv"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    rows, with_id, roles, first_id_at = 0, 0, {}, None
    for i, line in enumerate(text.splitlines()):
        if not line.strip():
            continue
        cols = line.split("\t")
        if i == 0 and cols[0].strip() == "when":
            continue
        rows += 1
        if len(cols) >= 5 and cols[4].strip():
            with_id += 1
            roles[cols[4].strip()] = cols[1].strip()
            when = cols[0].strip()
            if when and (first_id_at is None or when < first_id_at):
                first_id_at = when
    return {"rows": rows, "rowsWithId": with_id, "roles": roles,
            "firstIdAt": first_id_at}


def _spawn_rows(root=None):
    """How many rows the SubagentStart log carries, for the coverage pair."""
    c = spawn_census(root)
    return None if c is None else c["rows"]


# -------------------------------------------- E4: declared vs ran (a join)
# 2026-09-10 routing ruling, director follow-up: `.claude/agent-log.tsv`'s
# model column (log-agent.sh, same day) records what was ASKED FOR -- the
# SubagentStart payload's own `.model` field if the harness ever supplies
# one, else a `.claude/spawn-intent` sidecar, else the agent definition's
# own `model:` line -- NEVER what actually ran. What ran is recorded
# separately, at SubagentStop, in THIS file's `tier` column, keyed by
# `agentId`. Declared-versus-ran is therefore a JOIN on `agentId`, which is
# the reason that column is on both files, not a read of either alone.


def _declared_models(repo):
    """name -> declared `model:` value, front matter only, from the CURRENT
    `.claude/agents/*.md` files.

    A DELIBERATELY SMALLER READER than `ledger/verify.py`'s `_agent_model_
    defs` (the four-value gate, E1), which also classifies nonAgent/
    noModel/dupModel in detail for refusing a bad definition. This only
    needs a name-to-value map to compare against a RAN tier, and importing
    `ledger/verify.py` as a module from here was avoided on purpose: this
    session was told not to run that file, and keeping this a second,
    narrower, explicitly-justified reader is the safer reading of that
    instruction rather than sharing one through an import."""
    d = pathlib.Path(repo) / ".claude" / "agents"
    out = {}
    try:
        entries = sorted(d.glob("*.md"))
    except OSError:
        entries = []
    for f in entries:
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        if not lines or lines[0].strip() != "---":
            continue
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        for ln in (lines[1:end] if end else lines[1:]):
            m = re.match(r"^model:(.*)$", ln)
            if m:
                out[f.stem.strip().lower()] = m.group(1).strip()
                break
    return out


def _committed_model(repo, name):
    """The `model:` value committed at HEAD for agent `name`, or None when
    the file does not exist there or carries no recognisable line.

    Read via `git show HEAD:...` rather than the working tree, because the
    question this answers is "did the declaration change since the last
    commit", and that question needs BOTH snapshots."""
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), "show",
             "HEAD:.claude/agents/%s.md" % name],
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if p.returncode != 0:
        return None
    lines = p.stdout.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    for ln in (lines[1:end] if end else lines[1:]):
        m = re.match(r"^model:(.*)$", ln)
        if m:
            return m.group(1).strip()
    return None


def _ruling_cutovers(repo, decl):
    """name -> epoch seconds after which its CURRENT declared model applies,
    or None when there is none (every row in the turns log may be judged
    against it).

    A ROW BEFORE ITS AGENT'S CUTOVER CANNOT VIOLATE A RULE THAT DID NOT YET
    EXIST FOR THAT AGENT (the director's correction, 2026-09-10): the
    fable and opus disagreements below are real because producer,
    studio-director and the opus-declared builders have carried that exact
    declaration since before any logged spawn, so every row is fairly
    judged against it. Nine OTHER definitions (planner, content-wrangler
    and world-designer among them) were reclassified in the SAME session
    that built this check, so their pre-reclassification runs are being
    compared against a rule that postdates them -- a retroactive judgement,
    not a violation.

    MEASURED PER AGENT, NOT BY ONE GLOBAL TIMESTAMP: a single cutoff would
    also erase the two real buckets, since every one of their rows predates
    today's table edit too. What actually distinguishes them is whether
    THIS agent's declaration changed, checked against `git show HEAD:...`
    rather than the file's own mtime -- `producer.md` was edited again on
    2026-09-09 for a reason unrelated to its `model:` line (still `fable`
    both before and after), and a bare mtime comparison would have misread
    that edit as a reclassification it was not."""
    out = {}
    for name, cur in decl.items():
        committed = _committed_model(repo, name)
        if committed is None or committed == cur:
            out[name] = None
            continue
        f = pathlib.Path(repo) / ".claude" / "agents" / (name + ".md")
        try:
            out[name] = f.stat().st_mtime
        except OSError:
            out[name] = None
    return out


def _epoch(s):
    """One ISO8601 UTC stamp -> epoch seconds, or None. Mirrors
    `ledger/verify.py`'s `_cadence_epoch` in shape (same project, same
    contract: a bare `Z` offset, UTC assumed), kept as a second small
    reader rather than an import for the same reason `_declared_models`
    is its own reader and not a call into `ledger/verify.py`."""
    s = (s or "").strip()
    if not s:
        return None
    if s.endswith(("Z", "z")):
        s = s[:-1] + "+00:00"
    try:
        return datetime.datetime.fromisoformat(s).timestamp()
    except ValueError:
        return None


def routing_drift(repo=None):
    """DECLARED (what the definition asks for, TODAY) versus RAN (the LAST
    SubagentStop snapshot per `agentId`), joined on that column.

    THREE TRAPS MEASURED AND NAMED, each asserted against in the selftest
    so none can return silently:

      LAST-WINS, NEVER SUMMED. `agent-turns.tsv` writes one row per
      SubagentStop, and a spawn nudged past `maxTurns` writes SEVERAL rows
      for the SAME agentId with climbing turn counts (45, 68, 83, 105, 122,
      162 was a real sequence). Summed, that inflates one spawn's turns
      sixfold and the whole file's turns by roughly 2000 of 10407. This
      keeps only the LAST row written for each agentId (`read_log`'s own
      file order, which is chronological) and nothing else.

      NO DECLARATION, NO DISAGREEMENT. `general-purpose` and any other
      built-in `agent_type` with no `.claude/agents/<type>.md` on disk has
      nothing to compare against, and is counted in its OWN bucket, never
      as a violation (rule 3b: a fact this reader cannot judge is not the
      same fact as one it judged clean).

      PRE-RULING, NOT A VIOLATION. A row whose `when` predates its agent's
      OWN `_ruling_cutovers` entry is compliance with the rule as it THEN
      stood, not a disagreement with the rule as it stands now, and is
      counted in `preRuling` instead (see `_ruling_cutovers`'s own
      docstring for why this is per-agent and not one global timestamp,
      and why `preRuling` IS NOT ZERO AND NEVER WILL BE: the ruling
      reclassified nine definitions on the day it landed, so every run
      before that day was judged by a different table, permanently, and
      folding those rows back into the violation count the day this gap
      is "fixed" would be the exact fault this bucket exists to prevent).

    A FIRST DRAFT OF THIS FUNCTION MISSED THE THIRD TRAP and reported 37 of
    163 agents where the honest number was 24 of 163: it compared every
    historical row against TODAY's declaration with no notion that the
    declaration itself had a start date, so `planner`, `content-wrangler`
    and `world-designer`'s pre-reclassification opus runs read as
    violations of a rule that did not exist yet. Caught the same day by
    the director reading this function's own output against a hand tally
    that had excluded them correctly by knowing, by hand, which roles had
    just changed.

    Returns a dict, or `{"rows": None}` when the turns log could not be
    read at all."""
    base = pathlib.Path(repo) if repo else REPO
    decl = _declared_models(base)
    cutovers = _ruling_cutovers(base, decl)
    rows, _short, _unmeasured = read_log(log_path(base))
    if rows is None:
        return {"rows": None}
    last = {}
    for r in rows:
        if r.get("agentId") and r["agentId"] != "unknown":
            last[r["agentId"]] = r        # LAST occurrence wins: file order
    no_decl = []
    agreements = 0
    pre_ruling_rows = []
    pairs = {}                             # (declared, ran) -> [row, ...]
    for r in last.values():
        agent = r["agent"].strip().lower()
        ran = r["tier"].split("+")[0]             # strip a +mixed suffix
        d = decl.get(agent)
        if d is None:
            no_decl.append(agent)
            continue
        cutover = cutovers.get(agent)
        if cutover is not None:
            e = _epoch(r["when"])
            if e is None or e < cutover:
                # UNDATEABLE COUNTS AS PRE-RULING TOO: a row this reader
                # cannot place in time cannot be shown to postdate the
                # cutover either, and the safe direction (rule 5b) is the
                # one that never inflates a violation count.
                pre_ruling_rows.append(r)
                continue
        if d == ran:
            agreements += 1
            continue
        pairs.setdefault((d, ran), []).append(r)
    buckets = []
    disagree_agents = disagree_turns = 0
    for (d, ran), entries in pairs.items():
        n = len(entries)
        turns = sum(r["turns"] for r in entries)
        whens = sorted(r["when"] for r in entries)
        disagree_agents += n
        disagree_turns += turns
        buckets.append({"declared": d, "ran": ran, "agents": n,
                        "turns": turns, "whenMin": whens[0],
                        "whenMax": whens[-1]})
    buckets.sort(key=lambda b: -b["agents"])
    total_turns = sum(r["turns"] for r in last.values())
    return {"rows": True, "distinct": len(last), "agreements": agreements,
            "noDeclaration": len(no_decl),
            "noDeclarationNames": sorted(set(no_decl)),
            "preRuling": len(pre_ruling_rows),
            "preRulingTurns": sum(r["turns"] for r in pre_ruling_rows),
            "buckets": buckets, "disagreeAgents": disagree_agents,
            "disagreeTurns": disagree_turns, "totalTurns": total_turns}


def report_routing_drift(d):
    """The printed form of `routing_drift()`'s dict. Every number says what
    it is a statistic OF (rule: instruments.md), and the three that could
    be mistaken for each other -- violations, preRuling, noDeclaration --
    print as three separate counts so none can stand in for another (the
    director's own framing, 2026-09-10)."""
    if d.get("rows") is None:
        print("spawn-cost --routing-drift: %s (no turns log at %s)"
              % (NOTHING_MEASURED, log_path()))
        return 2
    print("spawn-cost --routing-drift: declared (today's .claude/agents/*.md) "
         "vs ran (last SubagentStop snapshot), joined on agentId")
    print("  distinct agentId(s) in the turns log, last-wins per id: %d"
          % d["distinct"])
    print("  agreements (declared == ran): %d" % d["agreements"])
    print("  preRuling=%d (%d turns): rows that predate the ruling for "
          "THEIR agent, compliance with the rule as it then stood, never a "
          "violation. NOT ZERO AND NEVER WILL BE: the 2026-09-10 ruling "
          "reclassified nine definitions the day it landed, so every run "
          "before that day was judged by a different table, permanently -- "
          "folding these rows back into the violation count would be the "
          "exact fault this bucket exists to prevent."
          % (d["preRuling"], d["preRulingTurns"]))
    print("  noDeclaration=%d excluded from the numerator (no .claude/"
          "agents/<type>.md on disk, so nothing to disagree with): %s"
          % (d["noDeclaration"],
             cap(d["noDeclarationNames"], keep=3) if d["noDeclarationNames"]
             else "none"))
    # DIRECTION DECIDES THE WORD, and the ruling is explicit about which
    # direction it restricts: "a spawn cannot override it upward without a
    # written reason". Downward is permitted and needs no reason. So a row that
    # ran BELOW its declared tier is not a violation of anything; it is a
    # SILENT DEMOTION, which matters for a different reason (a director
    # declared fable that ran opus was not the model the ruling asks for) and
    # must not be counted as rule-breaking. Only an upward run with no
    # resolving reason breaks the ruling as written.
    RANK = {"haiku": 0, "sonnet": 1, "opus": 2, "fable": 3}
    up, down = [], []
    for b in d["buckets"]:
        r_dec, r_ran = RANK.get(b["declared"], -1), RANK.get(b["ran"], -1)
        (up if r_ran > r_dec else down).append(b)
    if not d["buckets"]:
        print("  0 disagreement(s) of %d agent(s) examined" % d["distinct"])
    for b in down:
        print("  SILENT DEMOTION declared %s, ran %s (DOWNWARD, permitted "
              "without a reason): %d agent(s), %d turns, %s..%s"
              % (b["declared"], b["ran"], b["agents"], b["turns"],
                 b["whenMin"], b["whenMax"]))
    for b in up:
        print("  VIOLATION declared %s, ran %s (UPWARD, needs a resolving "
              "reason): %d agent(s), %d turns, %s..%s"
              % (b["declared"], b["ran"], b["agents"], b["turns"],
                 b["whenMin"], b["whenMax"]))
    print("  upwardWithoutReason=%d of %d bucket(s), which is what the ruling "
          "forbids; downwardUnrecorded=%d, which it permits"
          % (len(up), len(d["buckets"]), len(down)))
    print("  declared-versus-ran disagreements after the ruling, BOTH "
          "DIRECTIONS: %d of %d agent(s) (%.0f%%), "
          "%d of %d turn(s) (%.0f%%)"
          % (d["disagreeAgents"], d["distinct"],
             100.0 * d["disagreeAgents"] / d["distinct"] if d["distinct"] else 0,
             d["disagreeTurns"], d["totalTurns"],
             100.0 * d["disagreeTurns"] / d["totalTurns"]
             if d["totalTurns"] else 0))
    return 0



# ------------------------------- E370: the split, computed from the column
# WHICH SIDE AN AREA IS ON. This table is a JUDGEMENT and it is printed with
# every reading so that no reader has to take it on trust, because the fault
# queue 370 exists to fix is exactly a classification nobody could audit.
#
# It is a SECOND table and not a reuse of `ledger/verify.py`'s `DIRECTOR_WORK`
# on purpose, and the reason is the item's own sentence. `DIRECTOR_WORK`
# answers "does this path need a director review", whose `gated` flag tracks
# how expensive a wrong answer is, not who the work was for; borrowing it as
# a game/studio proxy would be a different quantity wearing the name, one
# layer along. What IS borrowed, because two copies of it would be the fault
# this project keeps paying for, is `GAME_AGENTS`: the role proxy below is
# the withdrawn reading and must be read from the one place that defines it.
GAME_LEDGER_DIRS = frozenset((
    "Assets", "CoreTests", "PerceptionGolden", "breaks", "Packages",
    "ProjectSettings"))
GAME_AREAS = frozenset(("content", "ue-probe", "voice-candidates"))
STUDIO_AREAS = frozenset((
    "tools", ".claude", ".github", ".githooks", "production", "ledger-v2",
    "research", "legacy", "game-design"))
# `.` (the repository root) IS DELIBERATELY UNCLASSIFIED: CLAUDE.md and
# canon.md sit there beside dashboard.html and STATUS.md, and calling that
# directory either side would be the guess this instrument replaces. It lands
# in `unclassified`, which is printed with its own count.
SIDE_GAME, SIDE_STUDIO, SIDE_UNKNOWN = "game", "studio", "unclassified"


def area_side(area):
    """One area -> game / studio / unclassified. Longest rule first."""
    a = (area or "").strip()
    if not a:
        return SIDE_UNKNOWN
    head = a.split("/")[0]
    if head == "ledger":
        parts = a.split("/")
        if len(parts) > 1 and parts[1] in GAME_LEDGER_DIRS:
            return SIDE_GAME
        # What is left of ledger/ after the game project is carved out is the
        # studio's own checkers and benches, which is the carve-out
        # `DIRECTOR_WORK`'s `ledgertools` entry already draws by hand.
        return SIDE_STUDIO
    if head in GAME_AREAS:
        return SIDE_GAME
    if head in STUDIO_AREAS:
        return SIDE_STUDIO
    return SIDE_UNKNOWN


def _roles(repo=None):
    """agentId -> role name, from `.claude/agent-log.tsv`. LAST-WINS per id.

    THE JOIN THAT MAKES THE LADDER POSSIBLE. `agent-log.tsv` is the only file
    that knows WHO a spawn was; the transcript does not carry `agent_type`
    (see `series`). Both rungs therefore read the same session set.

    One walker, in `spawn_census`: this map and the coverage denominators are
    two products of the same read, taken at the same instant."""
    c = spawn_census(repo)
    return {} if c is None else c["roles"]


def _game_agents():
    """(frozenset, source). The ROLE proxy's own table, read from the one
    place that defines it. On failure the caller prints the words and refuses
    rung 1 rather than carrying a second copy that could drift."""
    try:
        sys.path.insert(0, str(REPO / "ledger"))
        import verify as _v                                   # noqa: WPS433
        return frozenset(_v.GAME_AGENTS), "ledger/verify.py:GAME_AGENTS"
    except Exception:                                          # noqa: BLE001
        return None, NOTHING_MEASURED


def work_split(sessions, roles, game_agents, census=None):
    """The split, and every bucket it CANNOT answer, counted beside it.

    `sessions` is [{"agentId", "agent", "wrote"}]; LAST-WINS PER agentId, the
    same rule `routing_drift` takes and for the same measured reason (a spawn
    nudged past `maxTurns` writes several rows for one id).

    THE FOUR UNANSWERABLE BUCKETS ARE FOUR DIFFERENT FACTS and none of them
    is a zero:
      preColumn     the row was written before 2026-09-21. Permanent.
      transcriptGone the transcript was already gone at SubagentStop.
      noToolCall    the spawn called nothing: a slot spent on nothing.
      noFileWrite   tool calls were made, none was a file write. The session
                    worked through the shell, or only read. NOT "built
                    nothing", and the `fileToolsOfAll` pair beside it is what
                    separates those.

    AND A FIFTH THE FOUR ABOVE CANNOT SEE, which is why `census` exists.
    Those four are buckets of THIS file's rows, so their denominator is the
    stop log. A spawn that never reached SubagentStop wrote no row here at
    all: it is in no bucket, on no side, and invisible to `walked`. Queue
    370's sentence names the SPAWN log, so the spawn log's own census is
    passed in and `noStopRow` is counted against it. Measured on this
    machine 2026-09-21: 11 of 145 joinable spawn ids, and 530 of 747 spawn
    rows carry no id to join with in the first place.
    """
    last = {}
    for r in sessions:
        aid = (r.get("agentId") or "").strip()
        if not aid or aid == "unknown":
            continue
        last[aid] = r
    out = {"walked": len(last), "answerable": 0, "preColumn": 0,
           "transcriptGone": 0, "noToolCall": 0, "noFileWrite": 0,
           "areaCalls": {}, "hiddenAreas": 0, "hiddenCalls": 0,
           "sides": {SIDE_GAME: 0, SIDE_STUDIO: 0, "both": 0,
                     SIDE_UNKNOWN: 0},
           "roleGame": 0, "roleStudio": 0, "roleUnknown": 0,
           "cross": {}, "crossBoth": 0,
           # THE SPAWN LOG'S OWN DENOMINATORS, None when it could not be read
           # so the reader gets the words and not a zero.
           "spawnRows": None, "spawnRowsWithId": None, "spawnIds": None,
           "noStopRow": None, "noSpawnRow": None, "firstIdAt": None,
           "noSpawnRowPreId": None, "noSpawnRowSince": None}
    for aid, r in last.items():
        v = (r.get("wrote") or "").strip()
        if v == PRE_COLUMN or not v:
            out["preColumn"] += 1
        elif v == NOTHING_MEASURED:
            out["transcriptGone"] += 1
        elif v == WROTE_NO_TOOLS:
            out["noToolCall"] += 1
        elif v == WROTE_NONE:
            out["noFileWrite"] += 1
        areas, ha, hc = decode_touched(v)
        out["hiddenAreas"] += ha
        out["hiddenCalls"] += hc
        side_calls = {SIDE_GAME: 0, SIDE_STUDIO: 0, SIDE_UNKNOWN: 0}
        for a, n in areas.items():
            out["areaCalls"][a] = out["areaCalls"].get(a, 0) + n
            side_calls[area_side(a)] += n
        file_side = None
        if areas:
            out["answerable"] += 1
            g, st = side_calls[SIDE_GAME], side_calls[SIDE_STUDIO]
            if g and st:
                file_side = "both"
            elif g:
                file_side = SIDE_GAME
            elif st:
                file_side = SIDE_STUDIO
            else:
                file_side = SIDE_UNKNOWN
            out["sides"][file_side] += 1
        role = roles.get(aid) or r.get("agent") or ""
        role = role.strip().lower()
        if game_agents is None or not role or role == "unknown":
            out["roleUnknown"] += 1
            role_side = None
        elif role in game_agents:
            out["roleGame"] += 1
            role_side = SIDE_GAME
        else:
            out["roleStudio"] += 1
            role_side = SIDE_STUDIO
        if role_side and file_side:
            out["cross"][(role_side, file_side)] = \
                out["cross"].get((role_side, file_side), 0) + 1
            out["crossBoth"] += 1
    if census:
        # THE PAIRED READING, both directions, from the same two files in the
        # same run: how much of the spawn census this reading could see, and
        # how much of this reading the spawn census never heard of.
        spawn_ids = set(census["roles"])
        out["spawnRows"] = census["rows"]
        out["spawnRowsWithId"] = census["rowsWithId"]
        out["spawnIds"] = len(spawn_ids)
        out["noStopRow"] = len(spawn_ids - set(last))
        out["noSpawnRow"] = len(set(last) - spawn_ids)
        # AND SPLIT THAT SECOND NUMBER, because one total hides two facts.
        # A stop row older than the first id the spawn log ever recorded
        # COULD NEVER have joined; one newer than it means the start hook
        # missed a spawn that the stop hook saw, which is a live fault. The
        # boundary is read off the file, never pinned.
        out["firstIdAt"] = census.get("firstIdAt")
        if out["firstIdAt"]:
            out["noSpawnRowPreId"] = sum(
                1 for aid in set(last) - spawn_ids
                if (last[aid].get("when") or "") < out["firstIdAt"])
            out["noSpawnRowSince"] = out["noSpawnRow"] - out["noSpawnRowPreId"]
    return out


def report_work_split(d, source, game_src, header_note=None):
    """Every zero ships its denominator; every cap announces; and the two
    rungs are printed from the SAME session set in the SAME run, because a
    rung compared across runs is a different photograph."""
    print("spawn-cost --work-split: what each session WROTE, derived from "
          "its own transcript at SubagentStop and never self-reported")
    print("  source=%s gameAgentsFrom=%s" % (source, game_src))
    if header_note:
        print("  HEADER DRIFT: the live log's first line names %d column(s) "
              "and its rows now carry %d. Every reader here takes columns by "
              "POSITION, so no reading is wrong; a human running `head -1` "
              "gets stale names. The one-line correction, for a director to "
              "take (a builder does not edit a live log): %s"
              % (header_note[0], header_note[1], header_note[2]))
    if not d["walked"]:
        # The zero ships the other file's denominator: "no stop rows" beside
        # "N spawns happened" is a broken hook, and "no stop rows" beside "no
        # spawns" is a quiet week. One line must tell them apart.
        print("  %s: 0 session(s) to read, against spawnRowsCumulative=%s"
              % (NOTHING_MEASURED,
                 NOTHING_MEASURED if d["spawnRows"] is None
                 else d["spawnRows"]))
        return 2
    n = d["walked"]
    unans = (d["preColumn"] + d["transcriptGone"] + d["noToolCall"]
             + d["noFileWrite"])
    print("  sessions=%d (distinct agentId, LAST-WINS per id)" % n)
    print("  answerable=%d/%d  unanswerable=%d/%d" % (d["answerable"], n,
                                                      unans, n))
    print("    unanswerable, four facts and not one: preColumn=%d "
          "transcriptGone=%d noToolCall=%d noFileWrite=%d"
          % (d["preColumn"], d["transcriptGone"], d["noToolCall"],
             d["noFileWrite"]))
    print("    preColumn rows can NEVER answer: nothing rewrites a row and "
          "the transcript behind it went with its container")
    print("    noFileWrite is NOT a session that built nothing: a shell "
          "write is not recoverable from a transcript (measured 2026-09-21, "
          "6% precision over 348 candidate targets), so those sessions "
          "worked through the shell or only read")
    # COVERAGE AGAINST THE SPAWN LOG: a SECOND denominator, and the one queue
    # 370's sentence names. The four buckets above are buckets of stop-log
    # rows, so a spawn that never reached SubagentStop is in none of them.
    print("  COVERAGE AGAINST THE SPAWN LOG ITSELF (.claude/agent-log.tsv), "
          "a DIFFERENT denominator from `sessions` above:")
    if d["spawnRows"] is None:
        print("    %s: the spawn log could not be read, so how much of the "
              "spawn census this split saw is unknown -- NOT zero" %
              NOTHING_MEASURED)
    else:
        # CUMULATIVE over the file; ids are DISTINCT, last-wins per id.
        print("    spawnRowsCumulative=%d rowsCarryingAnId=%d/%d "
              "distinctSpawnIds=%d"
              % (d["spawnRows"], d["spawnRowsWithId"], d["spawnRows"],
                 d["spawnIds"]))
        print("      a spawn row with no id predates the agentId column and "
              "can be joined to nothing, ever: it is neither answerable nor "
              "unanswerable above, it is unreachable")
        # NO PUNCTUATION TOUCHING A VALUE. The first draft ended these two
        # tokens with a colon and `verify.py`'s reader took `11/145:` as the
        # number: every reader here splits on whitespace, so the prose starts
        # after a space or it is part of the value.
        print("    spawnIdsWithNoStopRow=%d/%d -- spawned, never reached "
              "SubagentStop, so in NO bucket above and on NO side below"
              % (d["noStopRow"], d["spawnIds"] or 0))
        print("    stopIdsWithNoSpawnRow=%d/%d -- the other direction, this "
              "reading sees sessions the spawn log never recorded an id for"
              % (d["noSpawnRow"], n))
        if d["noSpawnRowPreId"] is None:
            print("      of those, how many COULD have joined is %s: no spawn "
                  "row carries an id, so there is no instant to compare "
                  "against" % NOTHING_MEASURED)
        else:
            # ONE TOTAL, TWO FACTS. The pre-id half is structural and can
            # only hold still; the `since` half is the start hook missing a
            # spawn the stop hook saw, and it is the one worth an alarm.
            print("      splitAtFirstIdInSpawnLog=%s "
                  "predatingThatInstant=%d/%d (structural, can only hold "
                  "still) sinceThatInstant=%d/%d (the start hook missed a "
                  "spawn the stop hook saw)"
                  % (d["firstIdAt"], d["noSpawnRowPreId"], d["noSpawnRow"],
                     d["noSpawnRowSince"], d["noSpawnRow"]))
    if d["hiddenAreas"]:
        print("    the per-row cap BIT: +%d area(s) carrying %d write "
              "call(s) were collapsed into +Nmore cells, are counted in no "
              "area line below, AND ARE COUNTED ON NO SIDE: a biting cap can "
              "move a session from `both` to one side. AREAS_KEPT=%d was set "
              "above the measured peak so this clause should stay silent; it "
              "printing is the signal to re-read the series."
              % (d["hiddenAreas"], d["hiddenCalls"], AREAS_KEPT))
    areas = sorted(d["areaCalls"].items(), key=lambda kv: (-kv[1], kv[0]))
    print("  PER-AREA SERIES, CUMULATIVE write CALLS over the answerable "
          "sessions (not distinct files: two edits to one file are two):")
    if not areas:
        print("    %s: 0 area(s) over %d answerable session(s)"
              % (NOTHING_MEASURED, d["answerable"]))
    KEEP = 14
    for a, c in areas[:KEEP]:
        print("    %-34s %5d  %s" % (a, c, area_side(a)))
    if len(areas) > KEEP:
        print("    (+%d more not shown of %d, carrying %d call(s))"
              % (len(areas) - KEEP, len(areas),
                 sum(c for _, c in areas[KEEP:])))
    print("  RUNG 1, THE ROLE PROXY, which is the reading Jafar WITHDREW on "
          "2026-09-16 and which is printed here only as the rung to measure "
          "against: roleGame=%d/%d roleStudio=%d/%d roleUnknown=%d/%d"
          % (d["roleGame"], n, d["roleStudio"], n, d["roleUnknown"], n))
    s = d["sides"]
    a = d["answerable"]
    print("  RUNG 2, FROM WHAT WAS WRITTEN, over the ANSWERABLE sessions "
          "only: gameOnly=%d/%d studioOnly=%d/%d both=%d/%d "
          "unclassified=%d/%d"
          % (s[SIDE_GAME], a, s[SIDE_STUDIO], a, s["both"], a,
             s[SIDE_UNKNOWN], a))
    print("    `both` is a session the role proxy CANNOT express: one name "
          "per row, and a session that changed the game and the studio in "
          "one run lands wholly on whichever side its role name sits")
    print("  THE DIFFERENCE BETWEEN THE RUNGS, same session set, same run, "
          "over the %d session(s) that carry BOTH a role and a written area:"
          % d["crossBoth"])
    if not d["crossBoth"]:
        print("    %s: no session carries both" % NOTHING_MEASURED)
    for role_side in (SIDE_GAME, SIDE_STUDIO):
        for file_side in (SIDE_GAME, SIDE_STUDIO, "both", SIDE_UNKNOWN):
            c = d["cross"].get((role_side, file_side), 0)
            if c:
                mark = "agrees" if role_side == file_side else "DISAGREES"
                print("    roleSays=%-6s wroteIn=%-12s %4d  %s"
                      % (role_side, file_side, c, mark))
    agree = sum(c for (rs, fs), c in d["cross"].items() if rs == fs)
    print("    agree=%d/%d disagree=%d/%d -- THE PROXY ERROR, measured rather "
          "than estimated. Queue 370 put its size at \"32/110\" and "
          "\"12/27 where the answer was 1\" from two hand tallies; this is "
          "the same quantity counted." % (agree, d["crossBoth"],
                                          d["crossBoth"] - agree,
                                          d["crossBoth"]))
    print("  THE RATIO ITSELF IS NOT PRINTED HERE. Jafar withdrew it on "
          "2026-09-16 and whether it returns, and in what words, is his call "
          "or a director's at a close-out. This tool prints the counts the "
          "ratio would be built FROM, each beside what it could not answer.")
    if not d["answerable"]:
        # EXIT 2, NOT 0. Rung 1 printed and rung 2 did not: that is a reading
        # of the proxy, never a split, and the two outcomes must not share an
        # exit code. This is what a run against the live log returns until
        # spawns start landing rows that carry the column.
        print("  NOTHING MEASURED FOR RUNG 2: 0 of %d session(s) carry an "
              "answerable `wrote` value, so no split was computed. Exit 2."
              % d["walked"])
        return 2
    return 0


def sessions_from_transcripts(directory, root=None):
    """[{agentId, agent, wrote}] read straight off a directory of subagent
    transcripts: the PRINTER, exactly as `series` is, and the only way to get
    a reading today because the 325 rows already on disk predate the column
    and nothing rewrites them."""
    dd = pathlib.Path(directory)
    files = [f for f in sorted(dd.rglob("*.jsonl"))
             if f.parent.name == "subagents"] if dd.is_dir() else []
    out = []
    for f in files:
        t = read_transcript(f, root)
        aid = f.stem[len("agent-"):] if f.stem.startswith("agent-") else f.stem
        out.append({"agentId": aid, "agent": "unknown",
                    "wrote": t["wroteValue"],
                    "fileToolsOfAll": t["fileToolsValue"]})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--log", default=None, help="turns log to read")
    ap.add_argument("--transcripts", default=None,
                    help="directory of subagent .jsonl transcripts")
    ap.add_argument("--limit", type=int, default=0,
                    help="print at most N transcript lines (the cap announces "
                         "when it bites)")
    ap.add_argument("--hook", action="store_true",
                    help="SubagentStop: read the payload on stdin, append one "
                         "row, and ALWAYS exit 0")
    ap.add_argument("--work-split", action="store_true",
                    help="the studio-versus-game split from the `wrote` "
                         "column, printed WITH the count of rows it could "
                         "not answer for AND with the spawn census it could "
                         "not see at all (queue 370)")
    ap.add_argument("--routing-drift", action="store_true",
                    help="declared (definition) vs ran (turns log), joined "
                         "on agentId -- see routing_drift()")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if args.hook:
        try:
            hook(sys.stdin.read())
        except Exception:                                        # noqa: BLE001
            pass
        return 0
    if args.work_split:
        ga, ga_src = _game_agents()
        census = spawn_census()
        roles = {} if census is None else census["roles"]
        if args.transcripts:
            sess = sessions_from_transcripts(args.transcripts)
            src = "transcripts:" + str(args.transcripts)
            note = None
        else:
            rows, _s, _u = read_log(args.log or log_path())
            if rows is None:
                print("spawn-cost --work-split: %s (no turns log at %s)"
                      % (NOTHING_MEASURED, args.log or log_path()))
                return 2
            sess = rows
            src = str(args.log or log_path())
            note = header_drift(src)
        return report_work_split(work_split(sess, roles, ga, census), src,
                                 ga_src, note)
    if args.transcripts:
        return series(args.transcripts, args.limit)
    if args.routing_drift:
        return report_routing_drift(routing_drift())
    path = args.log or log_path()
    rows, short, unmeasured = read_log(path)
    return report(rows, short, str(path), _spawn_rows(), unmeasured)


if __name__ == "__main__":
    # A correct run that ends in a BrokenPipeError traceback costs twenty
    # minutes before anybody notices it worked.
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    sys.exit(main())
