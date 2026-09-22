#!/bin/bash
# Stop hook: A SITTING ENDS AT ITS TIME LIMIT OR WHEN THE LIST IS EMPTY.
#
# WHY THIS EXISTS. Jafar, 2026-09-22, verbatim: "You keep ending the sitting
# when one item gets hard, against the rule in CLAUDE.md, because a rule in a
# document cannot stop a turn from ending. Fix that mechanically, once, and it
# is the only piece of automation this session gets."
#
# It is an exception he made by name to CLAUDE.md's own "do not build anything
# whose purpose is to measure, report on, or enforce this session's own
# behaviour", and it is stripped to the one job: no wake queue, no records, no
# counters, nothing written anywhere. It reads NOW.md and decides. That is all.
#
# Contract (Claude Code Stop):
#   stdin:  { "hook_event_name":"Stop", "stop_hook_active":bool, ... }
#   exit 0  = let the turn end. Stdout is the hook's own line, on EVERY
#             outcome, because an allow is not an error.
#   exit 2  = BLOCK the stop; stderr is fed to Claude as the reason.
#
# THE LOOP HAZARD, and three things bound it:
#   1. stop_hook_active, honoured below: while the tool says the last stop was
#      already blocked by a hook, this permits. Without it a sitting with work
#      left could not be ended by anybody, including Jafar.
#   2. The platform overrides after 8 consecutive blocks
#      (CLAUDE_CODE_STOP_HOOK_BLOCK_CAP ?? 8).
#   3. The real loop-breaker: the work discharges the list. An item struck off
#      NOW.md is an item this no longer counts, and the time limit ends it
#      regardless of what is left.
#
# THE OPT-OUT IS SITTING_GUARD=off AND IT IS NEVER SILENT. settings.json
# travels with the repository, so any other checkout or headless run would
# otherwise be told to work down Jafar's list. Off permits, and says so.
#
# FAIL OPEN, DELIBERATELY AND OUT LOUD. A broken guard that BLOCKS is a
# session nobody can end; a broken guard that PERMITS costs one turn boundary.
# Every unexpected outcome below permits and names itself.

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOL="$REPO/tools/sitting-clock.py"

PAYLOAD="$(cat)"

if [ "${SITTING_GUARD:-on}" = "off" ]; then
    echo "sitting-continue: PERMIT reason=opted-out | SITTING_GUARD=off, so" \
         "the standing list was not read. This is not an empty list."
    exit 0
fi

if [ ! -f "$TOOL" ]; then
    echo "sitting-continue: PERMIT-UNASSESSED reason=tool-missing | the clock" \
         "could not run, so no list and no limit were read."
    exit 0
fi

# A REAL PYTHON, NOT THE FIRST NAME THAT ANSWERS. On this PC `python3` is the
# Windows Store alias: it prints "Python was not found" and EXITS 0, so a hook
# that trusted the name would permit every time and never say why. Each
# candidate has to actually evaluate something before it is used.
PY=""
for cand in python3 python py; do
    if [ "$($cand -c 'print(7*6)' 2>/dev/null)" = "42" ]; then
        PY="$cand"
        break
    fi
done
if [ -z "$PY" ]; then
    echo "sitting-continue: PERMIT-UNASSESSED reason=no-working-python | none" \
         "of python3, python or py could evaluate anything, so the clock did" \
         "not run and nothing was measured."
    exit 0
fi

# THE PAYLOAD IS NOT RE-TYPED HERE AND IT IS NOT GREPPED HERE. It goes to
# the tool, which parses it in the layer that has a selftest - the same
# choice, for the same reason, that the hook this is adapted from made. A
# hook that greps JSON for stop_hook_active is a hook that is wrong about
# a message containing a quotation mark, and the message is now something
# this has to READ rather than ignore. The loop guard moved with it.
LINE="$(printf '%s' "$PAYLOAD" | $PY "$TOOL" --hook 2>/dev/null)"
RC=$?

case "$RC" in
    2)
        # THE ONLY BLOCKING CODE. The reason goes to stderr, which is the
        # channel Claude Code feeds back to the model; the same line goes to
        # stdout so a human reading the transcript sees the verdict too.
        echo "sitting-continue: $LINE"
        echo "$LINE" >&2
        exit 2
        ;;
    0)
        echo "sitting-continue: $LINE"
        exit 0
        ;;
    *)
        echo "sitting-continue: PERMIT-UNASSESSED reason=unmodelled-exit" \
             "rc=$RC | the clock did not report a verdict this hook" \
             "understands, so the turn is allowed to end. This is not an" \
             "empty list."
        exit 0
        ;;
esac
