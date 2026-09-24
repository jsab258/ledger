#!/bin/bash
# Stop hook, one job (Jafar, 24 September): while the sitting has time and
# its list has an item left, keep going; otherwise stop. The deciding is
# in tools/sitting-clock.py, which reads NOW.md (SITTING line and list), for
# the builder's own session only. Exit 2 keeps the turn going (the reason goes
# to stderr); exit 0 lets it end. It fails open: anything unexpected permits.
# SITTING_GUARD=off turns it off, and says so.

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOL="$REPO/tools/sitting-clock.py"

PAYLOAD="$(cat)"

if [ "${SITTING_GUARD:-on}" = "off" ]; then
    echo "sitting-continue: PERMIT reason=opted-out | SITTING_GUARD=off, so" \
         "nothing was read."
    exit 0
fi

if [ ! -f "$TOOL" ]; then
    echo "sitting-continue: PERMIT-UNASSESSED reason=tool-missing | the clock" \
         "could not run, so nothing was read."
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
